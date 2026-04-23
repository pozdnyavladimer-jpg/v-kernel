from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

import numpy as np

from core.vkernel_engine import VKernelResult


@dataclass
class ModeClass:
    mode_id: int
    label: str
    description: str = ""
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class ClassificationResult:
    dominant_mode: int
    dominant_coefficient: float
    label: str
    description: str
    confidence: float
    mode_coefficients: np.ndarray
    metadata: Dict[str, str] = field(default_factory=dict)


class ModeClassifier:
    """
    Maps dominant graph modes to semantic labels / classes.

    This is the final output adapter:
        field evolution -> dominant mode -> interpretable result
    """

    def __init__(self, mode_map: Optional[Dict[int, ModeClass]] = None) -> None:
        self.mode_map = mode_map or self.default_mode_map()

    @staticmethod
    def default_mode_map() -> Dict[int, ModeClass]:
        return {
            1: ModeClass(
                mode_id=1,
                label="Binary Split",
                description="Two-lobed structural separation",
                metadata={"type": "dipole", "family": "split"},
            ),
            2: ModeClass(
                mode_id=2,
                label="Triangular Bias",
                description="Three-fold asymmetric distribution",
                metadata={"type": "triad", "family": "distribution"},
            ),
            3: ModeClass(
                mode_id=3,
                label="Quadrant Pattern",
                description="Four-region balance / opposition mode",
                metadata={"type": "quadrant", "family": "balance"},
            ),
            4: ModeClass(
                mode_id=4,
                label="Petal Resonance",
                description="Symmetric petal-like field organization",
                metadata={"type": "petal", "family": "resonance"},
            ),
            5: ModeClass(
                mode_id=5,
                label="Ring-Stable Mode",
                description="Cyclic / ring-oriented stabilization pattern",
                metadata={"type": "ring", "family": "cycle"},
            ),
            6: ModeClass(
                mode_id=6,
                label="High Symmetry Pattern",
                description="Higher-order symmetric structural mode",
                metadata={"type": "symmetric", "family": "harmonic"},
            ),
        }

    def register_mode(
        self,
        mode_id: int,
        label: str,
        description: str = "",
        metadata: Optional[Dict[str, str]] = None,
    ) -> None:
        self.mode_map[mode_id] = ModeClass(
            mode_id=mode_id,
            label=label,
            description=description,
            metadata=metadata or {},
        )

    def confidence_from_coefficients(
        self,
        coeffs: np.ndarray,
        dominant_mode: int,
        epsilon: float = 1e-8,
    ) -> float:
        coeffs = np.asarray(coeffs, dtype=float)
        total = float(np.sum(np.abs(coeffs))) + epsilon
        dominant = float(np.abs(coeffs[dominant_mode]))
        return dominant / total

    def classify_mode(
        self,
        dominant_mode: int,
        mode_coefficients: np.ndarray,
        dominant_coefficient: Optional[float] = None,
    ) -> ClassificationResult:
        coeffs = np.asarray(mode_coefficients, dtype=float)
        mode_info = self.mode_map.get(
            dominant_mode,
            ModeClass(
                mode_id=dominant_mode,
                label=f"Mode-{dominant_mode}",
                description="Unregistered stable mode",
            ),
        )

        if dominant_coefficient is None:
            dominant_coefficient = float(np.abs(coeffs[dominant_mode]))

        confidence = self.confidence_from_coefficients(coeffs, dominant_mode)

        return ClassificationResult(
            dominant_mode=dominant_mode,
            dominant_coefficient=dominant_coefficient,
            label=mode_info.label,
            description=mode_info.description,
            confidence=confidence,
            mode_coefficients=coeffs,
            metadata=mode_info.metadata,
        )

    def classify_result(self, result: VKernelResult) -> ClassificationResult:
        return self.classify_mode(
            dominant_mode=result.dominant_mode,
            mode_coefficients=result.mode_coefficients,
            dominant_coefficient=result.dominant_coefficient,
        )

    def summary_text(self, classification: ClassificationResult) -> str:
        return (
            f"Mode {classification.dominant_mode} -> {classification.label} | "
            f"confidence={classification.confidence:.3f} | "
            f"coefficient={classification.dominant_coefficient:.3f}"
            )

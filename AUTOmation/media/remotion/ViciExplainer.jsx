import { AbsoluteFill, Sequence, interpolate, useCurrentFrame, useVideoConfig, spring } from "remotion";
import { useMemo } from "react";

// ViciExplainer: animated explainer showing the AUTOmation pipeline flow
// Source -> AI -> Content -> Distribution

const stepColors = {
  source: "#ffffff",
  ai: "#00d4ff",
  content: "#00ff88",
  distribution: "#ff6b35",
};

export const ViciExplainer = ({
  title = "VICI / AUTOmation",
  steps = [
    { label: "Source", color: "#ffffff" },
    { label: "AI", color: "#00d4ff" },
    { label: "Content", color: "#00ff88" },
    { label: "Distribution", color: "#ff6b35" },
  ],
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();

  const totalStepDuration = Math.floor(durationInFrames / (steps.length + 1));

  const getStepProgress = (stepIndex) => {
    const stepStart = totalStepDuration * (stepIndex + 0.5);
    const stepEnd = stepStart + totalStepDuration;
    if (frame < stepStart) return 0;
    if (frame >= stepEnd) return 1;
    return (frame - stepStart) / totalStepDuration;
  };

  const getGlobalProgress = () => {
    return Math.min(Math.max((frame - 30) / (durationInFrames - 60), 0), 1);
  };

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%)",
        overflow: "hidden",
      }}
    >
      {/* Header */}
      <Sequence from={0} durationInFrames={60}>
        <AbsoluteFill
          style={{
            top: 80,
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <h1
            style={{
              color: "#ffffff",
              fontSize: interpolate(frame, [0, 30], [48, 48], { extrapolateLeft: "clamp" }),
              fontWeight: "bold",
              margin: 0,
              letterSpacing: "0.2em",
            }}
          >
            {title}
          </h1>
        </AbsoluteFill>
      </Sequence>

      {/* Animated arrow */}
      <Sequence from={60} durationInFrames={durationInFrames - 120}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
            flexDirection: "column",
          }}
        >
          {steps.map((step, index) => {
            const progress = getStepProgress(index);
            const opacity = interpolate(progress, [0, 0.2, 0.8, 1], [0.3, 0.3, 1, 1]);
            const scale = spring({
              fps,
              frame: frame - 60 - totalStepDuration * index,
              stiffness: 100,
              config: { mass: 0.5, damping: 15 },
              durationInFrames: 20,
            });

            const arrowOffset = interpolate(progress, [0, 1], [0, 40]);

            return (
              <div
                key={index}
                style={{
                  marginBottom: 40,
                  display: "flex",
                  alignItems: "center",
                  opacity,
                  transform: `scale(${scale})`,
                }}
              >
                {/* Step box */}
                <div
                  style={{
                    background: `linear-gradient(135deg, ${step.color}33, ${step.color}11)`,
                    border: `2px solid ${step.color}`,
                    borderRadius: 16,
                    padding: "24px 48px",
                    minWidth: 200,
                    textAlign: "center",
                  }}
                >
                  <div
                    style={{
                      color: step.color,
                      fontSize: 36,
                      fontWeight: "bold",
                      marginBottom: 8,
                    }}
                  >
                    {index + 1}
                  </div>
                  <div
                    style={{
                      color: "#ffffff",
                      fontSize: 24,
                    }}
                  >
                    {step.label}
                  </div>
                </div>

                {/* Arrow (except last step) */}
                {index < steps.length - 1 && (
                  <div
                    style={{
                      width: 60,
                      height: 3,
                      background: step.color,
                      margin: "0 20px",
                      position: "relative",
                      opacity: interpolate(progress, [0, 0.5, 1], [0, 0.5, 1]),
                    }}
                  >
                    <div
                      style={{
                        position: "absolute",
                        right: -10,
                        top: -8,
                        width: 0,
                        height: 0,
                        borderLeft: "12px solid transparent",
                        borderRight: "12px solid transparent",
                        borderBottom: `12px solid ${step.color}`,
                      }}
                    />
                  </div>
                )}
              </div>
            );
          })}
        </AbsoluteFill>
      </Sequence>

      {/* Footer */}
      <Sequence from={0} durationInFrames={durationInFrames}>
        <AbsoluteFill
          style={{
            bottom: 40,
            justifyContent: "flex-end",
            alignItems: "center",
          }}
        >
          <div
            style={{
              color: "#666666",
              fontSize: 16,
            }}
          >
            AUTOmation • Content Pipeline
          </div>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};

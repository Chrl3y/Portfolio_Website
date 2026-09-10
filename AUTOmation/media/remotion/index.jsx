import { Composition, registerRoot } from "remotion";
import { ViciExplainer } from "./ViciExplainer";
import { VideoSchema } from "./VideoSchema";

// Remotion 4.x entry point — uses registerRoot
registerRoot(() => (
  <Composition
    id="ViciExplainer"
    component={ViciExplainer}
    durationInFrames={180}
    fps={30}
    width={1920}
    height={1080}
    schema={VideoSchema}
    defaultProps={{ title: "AUTOmation", steps: ["Source", "AI", "Content", "Distribution"] }}
  />
));

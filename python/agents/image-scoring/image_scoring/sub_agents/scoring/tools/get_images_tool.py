from io import BytesIO
from PIL import Image
from google.adk.tools import ToolContext


def get_image(tool_context: ToolContext):
    artifact_name = (
        f"generated_image_" + str(tool_context.state.get("loop_iteration", 0)) + ".png"
    )
    artifact = tool_context.load_artifact(artifact_name)
    print(f" gcs image uri: {tool_context.state.get('generated_image_gcs_uri')}")
    metadata = {}

    if artifact and artifact.inline_data and artifact.inline_data.data:
        # open the image from image bytes with pillow
        image = Image.open(BytesIO(artifact.inline_data.data))

        # list all the image metadata attributes from image and assign it to variables
        metadata["size"] = image.size
        metadata["mode"] = image.mode
        metadata["format"] = image.format
        # metadata['info'] = str(image.info)

        # The image is loaded into the context by load_artifact.
        # We just need to return a JSON-serializable confirmation.
        print(f"Successfully loaded artifact: generated_image.png")

        # Option 1: Simple confirmation (Recommended)
        return {
            "status": "success",
            "message": f"Image artifact {artifact_name} successfully loaded.",
            "image_metadata": metadata,
        }

    else:
        print(f"Failed to load artifact or artifact has no inline data")
        return {
            "status": "error",
            "message": f"Could not load image artifact  or it was empty.",
        }

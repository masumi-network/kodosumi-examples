import fastapi
import uvicorn
import ray.serve as serve
import asyncio
import kodosumi.core as core
from kodosumi.core import forms as F

app = core.ServeAPI()

async def runner(inputs: dict):
    await asyncio.sleep(10)
    return {"result": "yes"}

@app.enter(
    path="/", 
    model=core.forms.Model(
        F.Markdown("# Simple Example"),
        F.Errors(),
        F.Break(),
        F.InputText(label="InputText", name="text"),
        F.InputFiles(label="Upload Files", name="files", multiple=True, 
                directory=False, required=False),
        F.Submit("Submit"),
        F.Cancel("Cancel"),
    ),
    summary="Simple Example",
    description="This services runs a simple job which actually does nothing but run.",
    version="1.0.0",
    author="m.rau@house-of-communication.com",
    tags=["Test"])
async def enter(request: fastapi.Request, inputs: dict):
    if str(inputs.get("text")).lower() != "yes":
        error = core.InputsError(f"Something went wrong with this input:<br/>{inputs}")
        error.add(text="you must say _yes_")
        raise error
    return core.Launch(request, "kodosumi_examples.simple.app.runner", inputs=inputs)


@serve.deployment
@serve.ingress(app)
class FormText: pass

fast_app = FormText.bind()  # type: ignore


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "kodosumi_examples.simple.app:app", 
        host="0.0.0.0", 
        port=8010, 
        reload=True
    )

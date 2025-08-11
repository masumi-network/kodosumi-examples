import kodosumi.core as core
from kodosumi.core import ServeAPI, forms as F
from kodosumi.response import Markdown
import fastapi
from typing import Optional
from ray import serve

app = ServeAPI()

async def simple_hitl_demo(inputs: dict, tracer: core.Tracer):
    """Simple HITL demonstration with minimal code"""
    
    # Show the input
    await tracer.markdown(f"### Input processed")
    await tracer.markdown(f"**Name:** {inputs.get('name', 'Not provided')}")
    await tracer.markdown(f"**Message:** {inputs.get('message', 'No message')}")
    
    # Collect human feedback
    feedback = await tracer.lock('simple_feedback')
    
    # Show result
    result = f"""
### HITL Demonstration Result

**Input processed successfully!**

**Human Feedback:**
- Rating: {feedback.get('rating', 'Not rated')}
- Comment: {feedback.get('comment', 'No comment')}

**Status:** ✅ Completed
"""
    
    return Markdown(result)

# Simple input form
input_form = core.forms.Model(
    F.Markdown("# Simple HITL Demonstration"),
    F.InputText(name="name", label="Your Name:", placeholder="John Doe"),
    F.InputArea(name="message", label="Your Message:", placeholder="Enter a message..."),
    F.Submit("Process"),
    F.Cancel("Cancel")
)

# Simple feedback form
feedback_form = core.forms.Model(
    F.Markdown("## Please rate the result:"),
    F.Select(
        name="rating",
        label="Rating:",
        option=[
            F.InputOption("good", "👍 Good"),
            F.InputOption("okay", "😐 Okay"),
            F.InputOption("bad", "👎 Bad")
        ]
    ),
    F.InputArea(name="comment", label="Comment (optional):", required=False),
    F.Submit("Send Feedback")
)

@app.enter(
    path="/",
    model=input_form,
    summary="Simple HITL Demo",
    description="Minimalist Human-in-the-Loop demonstration",
    version="1.0.0",
    author="example@kodosumi.com",
    tags=["HITL", "Simple", "Demo"]
)
async def enter(request: fastapi.Request, inputs: dict):
    return core.Launch(request, "kodosumi_examples.hitl.app:simple_hitl_demo", inputs=inputs)

@app.lock(name="simple_feedback")
async def collect_feedback(request: fastapi.Request, inputs: Optional[dict] = None):
    return feedback_form

@serve.deployment
@serve.ingress(app)
class HITLDemo: pass

fast_app = FormText.bind()  # type: ignore


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("kodosumi_examples.hitl.app:app", host="0.0.0.0", port=8015, reload=True) 
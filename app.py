import gradio as gr
from query import ask

#  HANDLER FUNCTION 
def handle_query(question):
    """
    Called every time the user clicks Ask or presses Enter.
    
    Takes the question string from the text box,
    passes it to ask(), and returns two strings:
    - the answer text
    - the formatted source list
    """
    
    # Don't process empty questions
    if not question.strip():
        return "Please enter a question.", ""
    
    # Call the full RAG pipeline
    result = ask(question)
    
    # Format sources as a bullet list
    sources = "\n".join(
        f"• {source}" for source in result["sources"]
    )
    
    return result["answer"], sources


# BUILD THE INTERFACE 
with gr.Blocks(
    title="NYU Math Unofficial Guide",
    theme=gr.themes.Soft()
) as demo:
    
    # Header
    gr.Markdown("""
    # NYU Mathematics Unofficial Guide
    Ask questions about NYU Math professors, courses, 
    and the mathematics program based on real student 
    reviews and Reddit discussions.
    """)
    
    # Input row
    with gr.Row():
        inp = gr.Textbox(
            label="Your Question",
            placeholder="e.g. What do students say about Pang's exams?",
            lines=2,
            scale=4
        )
    
    # Button
    btn = gr.Button("Ask", variant="primary")
    
    # Output row
    with gr.Row():
        answer_box = gr.Textbox(
            label="Answer",
            lines=8,
            scale=3
        )
        sources_box = gr.Textbox(
            label="Sources",
            lines=8,
            scale=1
        )
    
    # Example questions users can click
    gr.Examples(
        examples=[
            "What do students say about Pang's exams and grading curve?",
            "How does Professor Michael Shelley assess students?",
            "What are the difficulties of being a math major at NYU?",
            "What is it like being a math major at NYU Courant?",
            "Should I choose NYU for mathematics?"
        ],
        inputs=inp
    )
    
    # Wire up the button and Enter key
    btn.click(
        fn=handle_query,
        inputs=inp,
        outputs=[answer_box, sources_box]
    )
    inp.submit(
        fn=handle_query,
        inputs=inp,
        outputs=[answer_box, sources_box]
    )


# LAUNCH 
if __name__ == "__main__":
    print("Starting NYU Math Unofficial Guide...")
    print("Open your browser to: http://localhost:7860")
    demo.launch(inbrowser= True )

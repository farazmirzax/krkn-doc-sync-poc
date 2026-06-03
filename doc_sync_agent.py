# doc_sync_agent.py
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from mock_data import MOCK_UPSTREAM_DIFF

# Set up the local Ollama model
llm = OllamaLLM(model="llama3.2", temperature=0)

# Prompt used to generate the markdown table
gen_prompt = ChatPromptTemplate.from_template(
    "You are a Technical Documentation Generator Agent.\n"
    "Your job is to read this upstream Git Diff and generate a Hugo-compatible Markdown parameter table.\n"
    " convention: Columns must be | Parameter | Type | Default | Description |\n\n"
    "Git Diff:\n{diff}\n\n"
    "Previous Feedback (if any):\n{feedback}\n\n"
    "Generate only the Markdown table:"
)

# Prompt used to validate the generated table
val_prompt = ChatPromptTemplate.from_template(
    "You are a Strict Quality Assurance Agent.\n"
    "Compare the Generated Markdown Table against the Raw Git Diff source of truth.\n"
    "Check for:\n"
    "1. Hallucinations (Did it invent parameters or descriptions?)\n"
    "2. Discrepancies (Are the default values exact?)\n"
    "3. Missing fields.\n\n"
    "Raw Git Diff:\n{diff}\n\n"
    "Generated Markdown:\n{markdown}\n\n"
    "If it is 100% correct and accurate, reply with exactly: 'PASSED'.\n"
    "If there are issues, list the exact corrections needed."
)

def run_sync_loop():
    feedback = "None. This is the first attempt."
    max_iterations = 3
    
    print("🚀 Starting Doc Sync Agent Loop...\n")
    
    for i in range(max_iterations):
        print(f"--- Iteration {i+1} ---")
        
        # Generate the markdown table
        gen_chain = gen_prompt | llm
        generated_md = gen_chain.invoke({"diff": MOCK_UPSTREAM_DIFF, "feedback": feedback})
        print(f"[Generator Output]:\n{generated_md}\n")
        
        # Validate the generated markdown against the diff
        val_chain = val_prompt | llm
        validation_result = val_chain.invoke({"diff": MOCK_UPSTREAM_DIFF, "markdown": generated_md})
        print(f"[Validator Evaluation]:\n{validation_result}\n")
        
        # Stop early if validation passes
        if "PASSED" in validation_result.upper():
            print("✅ Validation Successful! The documentation is perfectly synced without drift.")
            break
        else:
            # Reuse validator feedback in the next attempt
            feedback = validation_result
    else:
        print("❌ Loop ended: Maximum iterations reached without explicit validation pass.")

if __name__ == "__main__":
    run_sync_loop()
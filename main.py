from parser import extract_query_components
from filter_data import filter_data
from data_utils import load_and_clean_pokedex
from nlg import generate_response
import gradio as gr

pokedex = load_and_clean_pokedex("data/pokedex.csv")

def chatbot_reply(message, history):
    parsed = extract_query_components(message)
    if "error" in parsed:
        return "Sorry, I couldn't understand your request. Try rephrasing it."
    filtered = filter_data(pokedex, parsed)
    response = generate_response(parsed, filtered)

    display_pokemon = filtered[["name", "type", parsed["stat"]]] if not filtered.empty else None
    return response, display_pokemon

with gr.Blocks(title="PokeGPT") as pokegpt:
    gr.Markdown("## 🧠 PokeGPT: Query Pokémon using natural language!")
    gr.Markdown("Try queries like:\n- `List all poison types with 50 or less attack`\n- `Fire types with hp over 100`")

    with gr.Row():
        chatbot = gr.Chatbot()
        dataframe_output = gr.Dataframe(label="Matching Pokémon", visible=True)

    msg = gr.Textbox(label="Enter your question")
    clear = gr.Button("Clear")

    state = gr.State([])

    def respond(message, history):
        response, table = chatbot_reply(message, history)
        history.append((message, response))
        return history, history, table

    msg.submit(respond, [msg, state], [chatbot, state, dataframe_output])
    clear.click(lambda: ([], [], None), None, [chatbot, state, dataframe_output])

pokegpt.launch()
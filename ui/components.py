import streamlit as st
import graphviz

def render_flow_graph(analysis_mode, current_style=None):
    """
    Renders a visual graph of the current analysis flow.
    """
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR', bgcolor='transparent')
    
    # Node Styles
    graph.attr('node', shape='box', style='filled', fillcolor='#161B22', fontcolor='white', color='#30363D', fontname='Inter')
    graph.attr('edge', color='#58a6ff')
    
    # Nodes
    graph.node('Input', 'Video Input\n(Frames)', shape='oval', fillcolor='#238636')
    graph.node('Gemini', 'Gemini 3\n(Reasoning)', shape='component', fillcolor='#8957e5')
    
    if analysis_mode == 'technical':
        graph.node('Output', 'Technical Analysis\n(Markdown)', shape='note')
        graph.edge('Input', 'Gemini')
        graph.edge('Gemini', 'Output', label='Extract Features')
        
    elif analysis_mode == 'creative_conversion':
        style_label = f"Style: {current_style}" if current_style else "Style Selection"
        graph.node('Style', style_label, shape='hexagon', fillcolor='#d29922', fontcolor='black')
        graph.node('Output', 'Creative Concept\n(Text)', shape='note')
        
        graph.edge('Input', 'Gemini')
        graph.edge('Style', 'Gemini', style='dashed')
        graph.edge('Gemini', 'Output', label='Re-imagine')
        
    elif analysis_mode == 'video_prompt':
        graph.node('Output', 'Video Gen Prompt\n(Wan 2.2/Sora)', shape='note')
        graph.edge('Input', 'Gemini')
        graph.edge('Gemini', 'Output', label='Optimize for Video')

    st.graphviz_chart(graph, use_container_width=True)

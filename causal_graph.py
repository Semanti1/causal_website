from graphviz import Digraph

all_sentences = [
['property:production', 'keyword:AND', 'property:connection to power source', 'keyword:is/are neccesary for', 'latent:Light'],
['property:stability', 'keyword:AND', 'property:extension', 'keyword:is/are neccesary for', 'latent:Lamp structure']
]
def process_causal(all_sentences):
    dot = Digraph()
    for sentence in all_sentences:
        property_list = []
        for field in sentence:
            name, value = field.split(':')
            if name == "property":
                dot.node(value, value);
                property_list.append(value);
            if name == "latent":
                dot.node(value, value);
                for property in property_list:
                    dot.edge(property, value);
    print(dot.source)
    #dot.render("output.gv", view=True)
    dot.save("output.gv")

#process_causal(all_sentences);

from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain


def run_research_pipeline(topic : str) -> dict:

    state = {}

    #search agent working
    print("\n"+"="*50)
    print("Step 1: Search agent is working!!!")
    print("="*50)


    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent and reliable information on the topic: {topic}")]
    })

    state["search_results"] = search_result['messages'][-1].content
    print("Search Results:\n", state["search_results"])


    #reader agent working
    print("\n"+"="*50)
    print("Step 2: Reader agent is scraping top resources!!!")
    print("="*50)

    reader_agent = build_reader_agent()

    reader_prompt = (
    f"Based on the following search about {topic}, "
    f"pick the most relevant URL and scrape it for deeper content.\n\n"
    f"Search Results:\n{state['search_results'][:800]}"
    )

    reader_result = reader_agent.invoke({
    "messages": [("user", reader_prompt)]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("Scraped Content:\n", state['scraped_content'])


    #Step 3 Writer chain
    print("\n"+"="*50)
    print("Step 3: Writer chain is drafting the research report!!!")
    print("="*50)


    research_combined = (
        f"SEARCH RESULTS: \n {state['search_results']}\n\n"
        f"DETAILED SCRAPPED CONTENT: \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n Final Report:\n", state['report'])


    #critic report
    print("\n"+"="*50)
    print("Step 4: Critic chain is reviewing the research report!!!")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report": state['report']
    })

    print("\n Critic Report:\n", state['feedback'])

    return state

if __name__ == "__main__":
    topic = input("\n Enter a research topic: ")
    run_research_pipeline(topic)

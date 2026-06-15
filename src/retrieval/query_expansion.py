class QueryExpander:
    """A minimal query expander.

    Can be configured to use synonyms, wordnet, or an LLM, but defaults to
    simply returning the query as-is to preserve offline functionality and
    avoid heavy dependencies unless explicitly requested.
    """
    def expand(self, query: str) -> list[str]:
        # For now, simply return the query itself.
        # In a full deployment, this would invoke an LLM or a thesaurus
        # to generate query variations (e.g., "remote work", "WFH").
        return [query]

import logging
from config import LLM_PROVIDER, LLM_MODEL
from mcp_servers.paper_search import paper_search
from mcp_servers.pdf_summarize import pdf_summarize

class AgentHost:
    """Receives user messages, routes to MCP servers, logs tool calls, and streams responses. Model-agnostic."""
    def __init__(self):
        self.llm_provider = LLM_PROVIDER
        self.llm_model = LLM_MODEL
        self.logger = logging.getLogger("AgentHost")
        self.logger.setLevel(logging.INFO)

    def log_tool_call(self, tool_name, args, outcome=None):
        self.logger.info(f"Tool call: {tool_name} | Args: {args} | Outcome: {outcome}")

    def handle_user_message(self, message):
        """Receives a user message, decides which MCP server(s) to call, and returns/streams the response."""
        # Simple keyword-based routing for demonstration
        if "search" in message.lower():
            query = message.replace("search", "").strip()
            args = {"query": query, "max_results": 5}
            self.log_tool_call("paper_search", args)
            result = paper_search(**args)
            self.log_tool_call("paper_search", args, outcome="success")
            return self.stream_response(result)
        elif "summarize" in message.lower():
            # Expecting: 'summarize <pdf_url>'
            parts = message.split()
            if len(parts) > 1:
                pdf_url = parts[1]
                args = {"pdf_url": pdf_url}
                self.log_tool_call("pdf_summarize", args)
                result = pdf_summarize(pdf_url)
                self.log_tool_call("pdf_summarize", args, outcome="success")
                return self.stream_response(result)
            else:
                return self.stream_response("Please provide a PDF URL to summarize.")
        else:
            return self.stream_response("Unknown command. Try 'search <topic>' or 'summarize <pdf_url>'.")

    def stream_response(self, response):
        """Streams the response back to the user (for CLI, yields lines)."""
        if isinstance(response, str):
            for line in response.splitlines():
                yield line
        elif isinstance(response, list):
            for item in response:
                if isinstance(item, dict):
                    # Pretty print paper search results
                    yield f"Title: {item.get('title')}"
                    yield f"Authors: {', '.join(item.get('authors', []))}"
                    yield f"Summary: {item.get('summary')[:300]}..."
                    yield f"Link: {item.get('link')}"
                    yield "---"
                else:
                    yield str(item)
        elif isinstance(response, dict):
            # For pdf_summarize output
            summary = response.get("summary", str(response))
            for line in summary.splitlines():
                yield line
        elif response is None:
            yield "No response."
        else:
            yield str(response) 
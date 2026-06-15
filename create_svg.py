def create_animated_svg(filepath):
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" width="100%" height="100%">
  <defs>
    <!-- Gradients -->
    <linearGradient id="agentGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4F46E5" />
      <stop offset="100%" stop-color="#7C3AED" />
    </linearGradient>
    <linearGradient id="dbGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#059669" />
      <stop offset="100%" stop-color="#10B981" />
    </linearGradient>
    <linearGradient id="llmGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#DC2626" />
      <stop offset="100%" stop-color="#EA580C" />
    </linearGradient>

    <!-- Pulse Animation for active nodes -->
    <style>
      .node { rx: 8px; ry: 8px; stroke-width: 2px; stroke: #fff; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.1)); }
      .text { font-family: system-ui, -apple-system, sans-serif; font-size: 14px; font-weight: 600; fill: #fff; text-anchor: middle; alignment-baseline: middle; dominant-baseline: middle; }
      .subtext { font-family: system-ui, -apple-system, sans-serif; font-size: 10px; fill: #E5E7EB; text-anchor: middle; alignment-baseline: middle; dominant-baseline: middle; }

      .arrow { stroke: #9CA3AF; stroke-width: 3px; fill: none; marker-end: url(#arrowhead); }

      /* Path animations */
      .path-pulse { stroke: #10B981; stroke-dasharray: 8 8; animation: dash 1s linear infinite; }
      @keyframes dash { to { stroke-dashoffset: -16; } }

      /* Node highlights sequential */
      @keyframes highlightPlan { 0%, 100% { filter: brightness(1); transform: scale(1); } 10%, 30% { filter: brightness(1.2) drop-shadow(0 0 10px #4F46E5); transform: scale(1.02); transform-origin: 100px 100px; } }
      @keyframes highlightRet { 0%, 100% { filter: brightness(1); transform: scale(1); } 30%, 50% { filter: brightness(1.2) drop-shadow(0 0 10px #4F46E5); transform: scale(1.02); transform-origin: 300px 100px; } }
      @keyframes highlightReas { 0%, 100% { filter: brightness(1); transform: scale(1); } 50%, 70% { filter: brightness(1.2) drop-shadow(0 0 10px #4F46E5); transform: scale(1.02); transform-origin: 500px 100px; } }
      @keyframes highlightResp { 0%, 100% { filter: brightness(1); transform: scale(1); } 70%, 90% { filter: brightness(1.2) drop-shadow(0 0 10px #4F46E5); transform: scale(1.02); transform-origin: 700px 100px; } }

      #planner { animation: highlightPlan 4s infinite; }
      #retriever { animation: highlightRet 4s infinite; }
      #reasoner { animation: highlightReas 4s infinite; }
      #responder { animation: highlightResp 4s infinite; }

      /* Data flow packets */
      @keyframes movePacket1 { 0% { offset-distance: 0%; opacity: 0; } 10% { opacity: 1; } 25% { offset-distance: 100%; opacity: 0; } 100% { offset-distance: 100%; opacity: 0; } }
      @keyframes movePacket2 { 0%, 25% { offset-distance: 0%; opacity: 0; } 30% { opacity: 1; } 45% { offset-distance: 100%; opacity: 0; } 100% { offset-distance: 100%; opacity: 0; } }
      @keyframes movePacket3 { 0%, 45% { offset-distance: 0%; opacity: 0; } 50% { opacity: 1; } 65% { offset-distance: 100%; opacity: 0; } 100% { offset-distance: 100%; opacity: 0; } }
      @keyframes movePacket4 { 0%, 65% { offset-distance: 0%; opacity: 0; } 70% { opacity: 1; } 85% { offset-distance: 100%; opacity: 0; } 100% { offset-distance: 100%; opacity: 0; } }

      .packet { fill: #10B981; r: 6; filter: drop-shadow(0 0 4px #10B981); }
      .p1 { offset-path: path("M160,100 L240,100"); animation: movePacket1 4s linear infinite; }
      .p2 { offset-path: path("M360,100 L440,100"); animation: movePacket2 4s linear infinite; }
      .p3 { offset-path: path("M560,100 L640,100"); animation: movePacket3 4s linear infinite; }
    </style>

    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#9CA3AF" />
    </marker>
  </defs>

  <rect width="100%" height="100%" fill="#111827" />

  <text x="400" y="30" font-family="system-ui" font-size="24" font-weight="700" fill="#fff" text-anchor="middle">KnowledgeX Agentic Workflow</text>
  <text x="400" y="55" font-family="system-ui" font-size="14" fill="#9CA3AF" text-anchor="middle">LangGraph Orchestration &amp; Advanced Retrieval</text>

  <!-- Connectors -->
  <!-- Planner to Retriever -->
  <path d="M 160 100 L 240 100" class="arrow path-pulse" />
  <text x="200" y="90" class="subtext">Queries</text>

  <!-- Retriever to Reasoner -->
  <path d="M 360 100 L 440 100" class="arrow path-pulse" />
  <text x="400" y="90" class="subtext">Chunks</text>

  <!-- Reasoner to Responder -->
  <path d="M 560 100 L 640 100" class="arrow path-pulse" />
  <text x="600" y="90" class="subtext">Pass</text>

  <!-- Reasoner to Planner (Retry Loop) -->
  <path d="M 500 140 C 500 180, 100 180, 100 140" class="arrow" stroke-dasharray="4 4" />
  <text x="300" y="175" class="subtext" fill="#EF4444">Fail (Retry)</text>

  <!-- External Connections -->
  <path d="M 300 140 L 300 240" class="arrow" />
  <path d="M 300 240 L 300 140" class="arrow path-pulse" />

  <path d="M 700 140 L 700 240" class="arrow" />
  <path d="M 700 240 L 700 140" class="arrow path-pulse" />

  <!-- Nodes -->
  <!-- Planner -->
  <g id="planner">
    <rect x="40" y="60" width="120" height="80" fill="url(#agentGrad)" class="node" />
    <text x="100" y="95" class="text">Planner</text>
    <text x="100" y="115" class="subtext">Query Decomp.</text>
  </g>

  <!-- Retriever -->
  <g id="retriever">
    <rect x="240" y="60" width="120" height="80" fill="url(#agentGrad)" class="node" />
    <text x="300" y="95" class="text">Retriever</text>
    <text x="300" y="115" class="subtext">Hybrid + Rerank</text>
  </g>

  <!-- Reasoner -->
  <g id="reasoner">
    <rect x="440" y="60" width="120" height="80" fill="url(#agentGrad)" class="node" />
    <text x="500" y="95" class="text">Reasoner</text>
    <text x="500" y="115" class="subtext">Eval Confidence</text>
  </g>

  <!-- Responder -->
  <g id="responder">
    <rect x="640" y="60" width="120" height="80" fill="url(#agentGrad)" class="node" />
    <text x="700" y="95" class="text">Responder</text>
    <text x="700" y="115" class="subtext">Generation</text>
  </g>

  <!-- Data Sources -->
  <g id="database">
    <rect x="220" y="240" width="160" height="80" fill="url(#dbGrad)" class="node" />
    <text x="300" y="270" class="text">Enterprise Index</text>
    <text x="300" y="290" class="subtext">ChromaDB + BM25</text>
  </g>

  <!-- LLM Provider -->
  <g id="llms">
    <rect x="620" y="240" width="160" height="80" fill="url(#llmGrad)" class="node" />
    <text x="700" y="270" class="text">LLM Providers</text>
    <text x="700" y="290" class="subtext">Ollama / Anthropic</text>
  </g>

  <!-- Observability Overlay -->
  <rect x="20" y="340" width="760" height="40" fill="#374151" class="node" rx="4" ry="4" stroke="none" />
  <text x="400" y="360" class="text" font-size="12">Telemetry &amp; Tracing: OpenTelemetry • Langfuse • Prometheus</text>

  <!-- Animated Packets -->
  <circle class="packet p1" cx="0" cy="0" />
  <circle class="packet p2" cx="0" cy="0" />
  <circle class="packet p3" cx="0" cy="0" />
</svg>
"""
    with open(filepath, "w") as f:
        f.write(svg_content)
    print(f"Created SVG at {filepath}")

if __name__ == "__main__":
    import sys
    create_animated_svg(sys.argv[1])

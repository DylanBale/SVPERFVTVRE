#!/usr/bin/env python3
"""Generate model profile pages and comparison pages for svperfvtvre.com"""

import os

OUTPUT_DIR = "/home/claude/svperfvtvre"

# ═══════════════ SHARED CSS ═══════════════
SHARED_CSS = """
:root {
  --bg-primary: #0a0a0a;
  --bg-secondary: #111111;
  --bg-tertiary: #1a1a1a;
  --text-primary: #e8e8e8;
  --text-secondary: #888888;
  --text-muted: #555555;
  --accent: #63b3ed;
  --accent-bright: #90cdf4;
  --accent-dim: #2b6cb0;
  --accent-glow: rgba(99, 179, 237, 0.15);
  --border: #1e1e1e;
  --border-hover: #2d2d2d;
  --success: #68d391;
  --warning: #f6ad55;
  --error: #fc8181;
  --font-display: 'Syne', sans-serif;
  --font-body: 'DM Sans', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: var(--font-body); background: var(--bg-primary); color: var(--text-primary); line-height: 1.7; }
.container { max-width: 800px; margin: 0 auto; padding: 0 1.5rem; }
a { color: var(--accent); text-decoration: none; }
a:hover { color: var(--accent-bright); }
.site-header { padding: 2rem 0 1rem; text-align: center; border-bottom: 1px solid var(--border); margin-bottom: 2rem; }
.logo { font-family: var(--font-display); font-size: 1.6rem; font-weight: 600; letter-spacing: 0.15em; background: linear-gradient(135deg, #4a5568 0%, #a0aec0 30%, #63b3ed 50%, #a0aec0 70%, #4a5568 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; display: inline-block; }
.breadcrumb { font-size: 0.8rem; color: var(--text-muted); margin-bottom: 2rem; }
.breadcrumb a { color: var(--text-muted); }
.breadcrumb a:hover { color: var(--accent); }
h1 { font-family: var(--font-display); font-size: 2rem; font-weight: 600; margin-bottom: 0.5rem; }
h2 { font-family: var(--font-display); font-size: 1.4rem; font-weight: 500; margin: 2rem 0 1rem; color: var(--text-primary); }
h3 { font-size: 1rem; font-weight: 500; margin: 1.5rem 0 0.5rem; }
p { margin-bottom: 1rem; color: var(--text-secondary); }
.version-badge { font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent); background: var(--accent-glow); padding: 0.2rem 0.6rem; display: inline-block; margin-bottom: 1rem; }
.company { font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.5rem; }
.specs-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin: 1.5rem 0; }
.spec-card { background: var(--bg-secondary); border: 1px solid var(--border); padding: 1rem; }
.spec-label { font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.3rem; }
.spec-value { font-size: 1rem; font-weight: 500; }
.pros-cons { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin: 1.5rem 0; }
.pros h3, .cons h3 { margin-top: 0; }
.pros li, .cons li { font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.4rem; padding-left: 0.5rem; list-style: none; }
.pros li::before { content: '✓ '; color: var(--success); }
.cons li::before { content: '✗ '; color: var(--error); }
.cta-section { margin: 2rem 0; padding: 1.5rem; background: var(--bg-secondary); border: 1px solid var(--border); text-align: center; }
.cta-btn { display: inline-flex; align-items: center; gap: 0.5rem; background: var(--accent); color: var(--bg-primary); padding: 0.75rem 2rem; font-size: 1rem; font-weight: 600; text-decoration: none; transition: background 0.2s; font-family: var(--font-body); }
.cta-btn:hover { background: var(--accent-bright); color: var(--bg-primary); }
.nav-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 2rem 0; }
.nav-card { background: var(--bg-secondary); border: 1px solid var(--border); padding: 1rem; transition: border-color 0.2s; }
.nav-card:hover { border-color: var(--accent-dim); }
.nav-card-label { font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.06em; }
.nav-card-name { font-weight: 500; margin-top: 0.2rem; }
.site-footer { margin-top: 3rem; padding: 2rem 0; border-top: 1px solid var(--border); text-align: center; font-size: 0.75rem; color: var(--text-muted); }
.site-footer a { color: var(--text-muted); margin: 0 0.5rem; }
/* Comparison specific */
.compare-table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; }
.compare-table th { text-align: left; font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.06em; padding: 0.75rem; border-bottom: 1px solid var(--border); }
.compare-table td { padding: 0.75rem; border-bottom: 1px solid var(--border); font-size: 0.9rem; color: var(--text-secondary); }
.compare-table td:first-child { color: var(--text-muted); font-size: 0.8rem; }
.winner { color: var(--accent) !important; font-weight: 500; }
.verdict { background: var(--bg-secondary); border: 1px solid var(--border); padding: 1.5rem; margin: 2rem 0; }
.verdict h3 { margin-top: 0; color: var(--accent); }
@media (max-width: 640px) { .pros-cons { grid-template-columns: 1fr; } .nav-cards { grid-template-columns: 1fr; } .specs-grid { grid-template-columns: 1fr; } }
"""

FONTS_LINK = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'

# ═══════════════ MODEL DATA ═══════════════
MODELS = {
    "claude": {
        "name": "Claude",
        "version": "Opus 4.5 / Sonnet 4.5 / Haiku 4.5",
        "company": "Anthropic",
        "url": "https://claude.ai",
        "pricing": "Free tier / $20/mo (Pro) / $30/mo (Team)",
        "context": "200K tokens",
        "bestFor": "Writing, Coding, Analysis, Reasoning",
        "title": "Claude AI Review 2026 — Opus 4.5, Sonnet 4.5 & Haiku",
        "meta_desc": "Complete Claude AI review for 2026. Compare Opus 4.5, Sonnet 4.5, and Haiku models. Pricing, features, context windows, and best use cases.",
        "meta_keywords": "Claude AI review, Claude Opus 4.5, Claude vs ChatGPT, Anthropic Claude, Claude pricing 2026, best AI for writing",
        "intro": "Claude by Anthropic has become one of the most respected AI assistants, known for producing thoughtful, well-structured outputs that follow complex instructions with remarkable accuracy. The Claude 4.5 family — Opus, Sonnet, and Haiku — covers everything from quick daily tasks to deep reasoning and complex coding projects.",
        "details": "Claude Opus 4.5 is the flagship model, excelling at nuanced writing, complex code refactoring, and tasks that require careful reasoning. It's consistently rated as one of the top models for coding benchmarks and is widely used by developers via Claude Code, Anthropic's CLI coding agent. Sonnet 4.5 hits the sweet spot between speed and capability — fast enough for daily use, capable enough for serious work. It's the default model most people interact with on claude.ai. Haiku 4.5 is the speed-optimized option, perfect for high-volume API usage where cost and latency matter more than peak intelligence.",
        "pros": ["Exceptional writing quality and instruction-following", "Claude Code CLI is a top-tier agentic coding tool", "200K context window handles long documents well", "Strong safety track record and thoughtful outputs", "Generous free tier for casual use"],
        "cons": ["No native web search (uses tools instead)", "Image generation not built-in", "Opus can be slower than competitors for simple tasks", "API pricing higher than DeepSeek for high-volume use"],
        "best_for_sections": "Claude shines brightest for professional writing (reports, emails, marketing copy), complex coding tasks (architecture decisions, refactoring, code review), research synthesis (analyzing long documents and extracting insights), and any task where following nuanced instructions matters.",
        "competitors": [("chatgpt", "ChatGPT"), ("gemini", "Gemini")],
        "compare_link": "/compare/claude-vs-chatgpt.html"
    },
    "chatgpt": {
        "name": "ChatGPT",
        "version": "GPT-5.2",
        "company": "OpenAI",
        "url": "https://chat.openai.com",
        "pricing": "$8/mo (Go) / $20/mo (Plus) / $200/mo (Pro)",
        "context": "400K tokens",
        "bestFor": "General purpose, Math, Reasoning, Coding",
        "title": "ChatGPT GPT-5.2 Review 2026 — Features, Pricing & Use Cases",
        "meta_desc": "Complete ChatGPT GPT-5.2 review for 2026. New 400K context window, perfect math scores, and 40% fewer hallucinations. Pricing tiers, features, and comparisons.",
        "meta_keywords": "ChatGPT review 2026, GPT-5.2, ChatGPT Plus, ChatGPT vs Claude, OpenAI GPT-5, best AI chatbot",
        "intro": "ChatGPT remains the most widely used AI assistant in the world, and GPT-5.2 represents a significant leap forward. With a 400K token context window, perfect AIME 2025 math scores, and a 40% reduction in hallucinations, it's more capable and reliable than ever.",
        "details": "GPT-5.2 brings several major improvements: the context window has tripled from 128K to 400K tokens, math reasoning is now near-perfect on standard benchmarks, and hallucination rates have dropped significantly. OpenAI also introduced ChatGPT Go at $8/month — a speed-optimized tier for users who want the basics at a lower price. The Plus tier ($20/month) remains the mainstream option with full access to GPT-5.2, image generation via GPT-4o, Sora video generation, and DALL-E. The Pro tier ($200/month) unlocks unlimited access and priority during peak times. OpenAI also released GPT-oss open-weight models (120B and 20B parameters) under Apache 2.0 license — a major shift toward open source.",
        "pros": ["Most versatile general-purpose AI", "400K context window (largest among closed models)", "Native image generation and video (Sora 2)", "Multiple pricing tiers including $8/mo Go option", "Huge ecosystem of plugins, GPTs, and integrations"],
        "cons": ["Plus tier still $20/mo for full features", "Can be verbose compared to Claude", "Image generation less artistic than Midjourney", "Pro tier at $200/mo is expensive"],
        "best_for_sections": "ChatGPT is the best all-rounder for users who need one tool for everything: writing, coding, math, data analysis, image generation, and general conversation. The breadth of its capabilities and ecosystem (custom GPTs, plugins, API) make it the default choice for most people.",
        "competitors": [("claude", "Claude"), ("gemini", "Gemini")],
        "compare_link": "/compare/claude-vs-chatgpt.html"
    },
    "gemini": {
        "name": "Gemini",
        "version": "3 Pro",
        "company": "Google",
        "url": "https://gemini.google.com",
        "pricing": "Free / $20/mo (Advanced)",
        "context": "1M tokens",
        "bestFor": "Research, Long documents, Multimodal",
        "title": "Google Gemini 3 Pro Review 2026 — #1 on LM Arena",
        "meta_desc": "Gemini 3 Pro review for 2026. #1 on LM Arena rankings with 1M token context window. Free tier, Google integration, and multimodal capabilities.",
        "meta_keywords": "Gemini 3 Pro review, Google Gemini, best free AI, Gemini vs ChatGPT, 1M context window, best AI for research",
        "intro": "Google's Gemini 3 Pro has claimed the #1 position on LM Arena's human preference rankings with a score of 1490 — the highest of any model. Combined with its massive 1 million token context window and deep Google ecosystem integration, it's become a formidable competitor.",
        "details": "The 1M token context window is Gemini's killer feature — you can feed it entire codebases, books, or months of documents and it maintains coherence throughout. Google integration means it works seamlessly with Drive, Docs, Gmail, and YouTube. The free tier is remarkably generous, making it the best no-cost option for many users. Multimodal capabilities span text, images, audio, and video understanding. Recent updates have improved creative writing and tool use based on direct user feedback.",
        "pros": ["#1 on LM Arena human preference rankings", "1M token context — largest available", "Most generous free tier among major models", "Deep Google Workspace integration", "Strong multimodal understanding"],
        "cons": ["Google ecosystem lock-in for best experience", "Creative writing historically weaker (improving)", "Agent mode less reliable on complex refactors", "Advanced features require $20/mo subscription"],
        "best_for_sections": "Gemini is the clear choice for analyzing massive documents (entire codebases, research papers, books), Google Workspace power users, budget-conscious users who want top-tier AI for free, and multimodal tasks involving video or audio understanding.",
        "competitors": [("chatgpt", "ChatGPT"), ("claude", "Claude")],
        "compare_link": ""
    },
    "grok": {
        "name": "Grok",
        "version": "4.1",
        "company": "xAI",
        "url": "https://x.ai",
        "pricing": "$8/mo (X Premium) / Free on X",
        "context": "128K tokens",
        "bestFor": "Reasoning, Real-time social data, Low hallucination",
        "title": "Grok 4.1 Review 2026 — #1 Reasoning, Lowest Hallucination Rate",
        "meta_desc": "Grok 4.1 review for 2026. Top LMArena Elo (1483), only 4% hallucination rate. Real-time X/social integration. Pricing, features, comparisons.",
        "meta_keywords": "Grok 4.1 review, xAI Grok, Grok vs ChatGPT, best AI reasoning, low hallucination AI",
        "intro": "Grok 4.1 from xAI has quietly become one of the most impressive models available. It holds the #1 position on LMArena Elo rankings (1483) and EQ-Bench, with a hallucination rate of just 4% — a 65% reduction from its predecessor.",
        "details": "In blind A/B tests, users preferred Grok 4.1 responses nearly 65% of the time over the previous model. Its deep integration with X (formerly Twitter) gives it unique access to real-time social data, trending topics, and current events. For developers, Grok Code Fast 1 is a specialized model built for agentic coding workflows. The biggest story is reliability — at 4% hallucination rate, Grok 4.1 is the most factually reliable major model currently available.",
        "pros": ["Lowest hallucination rate (4%) among major models", "#1 LMArena Elo and EQ-Bench rankings", "Real-time X/social media integration", "Affordable via X Premium ($8/mo)", "Strong reasoning and logic capabilities"],
        "cons": ["Smaller ecosystem than ChatGPT/Claude", "X integration may not matter for all users", "Less proven for long-form writing", "Context window smaller than GPT-5.2 and Gemini"],
        "best_for_sections": "Grok excels at tasks requiring high factual accuracy, real-time social media analysis, reasoning-heavy problems, and situations where hallucinations are unacceptable (e.g., factual reports, data interpretation).",
        "competitors": [("chatgpt", "ChatGPT"), ("claude", "Claude")],
        "compare_link": ""
    },
    "perplexity": {
        "name": "Perplexity",
        "version": "Pro",
        "company": "Perplexity AI",
        "url": "https://perplexity.ai",
        "pricing": "Free / $20/mo (Pro) / $50/mo (Enterprise)",
        "context": "Web-sourced",
        "bestFor": "Research, Citations, Fact-checking, Current events",
        "title": "Perplexity AI Review 2026 — Best AI for Research & Citations",
        "meta_desc": "Perplexity AI review for 2026. The best AI search engine for cited, sourced research. Deep Research mode, Pro features, and pricing compared.",
        "meta_keywords": "Perplexity AI review, best AI for research, Perplexity vs Google, AI search engine, cited AI answers",
        "intro": "Perplexity is the AI you use when you need answers you can verify. Unlike traditional chatbots that generate responses from training data, Perplexity actively searches the web and provides citations for every claim — making it the gold standard for research.",
        "details": "The Deep Research mode is Perplexity's standout feature — it conducts multi-step research across dozens of sources, synthesizes findings, and presents them with full citations. The Pro tier unlocks unlimited Deep Research queries, file uploads, and access to multiple underlying models. The free tier is surprisingly capable for basic research. Enterprise tiers ($50-325/mo) add team features, SOC2 compliance, and API access.",
        "pros": ["Every response includes verifiable citations", "Deep Research mode for comprehensive analysis", "Real-time web search for current information", "Clean, focused interface", "Strong free tier for basic research"],
        "cons": ["Not great for creative writing or coding", "Deep Research can be slow (minutes)", "Citation accuracy isn't always perfect", "Pro features behind $20/mo paywall"],
        "best_for_sections": "Perplexity is the clear winner for anyone who needs sourced answers: journalists, students, analysts, marketers doing competitive research, and anyone who needs to verify claims before sharing them.",
        "competitors": [("gemini", "Gemini"), ("grok", "Grok")],
        "compare_link": ""
    },
    "cursor": {
        "name": "Cursor",
        "version": "Latest",
        "company": "Cursor",
        "url": "https://cursor.com",
        "pricing": "Free / $20/mo (Pro) / $40/mo (Business)",
        "context": "Full codebase",
        "bestFor": "AI-native IDE, Agentic coding, Full-stack development",
        "title": "Cursor Review 2026 — The AI-Native Code Editor",
        "meta_desc": "Cursor IDE review for 2026. AI-native code editor with agentic coding, full codebase understanding, and multi-file refactoring. Pricing, features, vs Windsurf.",
        "meta_keywords": "Cursor review, Cursor vs Windsurf, AI code editor, best AI for coding, Cursor IDE, agentic coding",
        "intro": "Cursor has redefined what a code editor can be. Built on VS Code but reimagined for AI, it understands your entire codebase and can autonomously handle multi-file refactors, bug fixes, and feature implementation.",
        "details": "Cursor's Agent mode is what sets it apart — instead of just suggesting code, it can plan and execute multi-step changes across your entire project. It reads your codebase, understands the architecture, and makes changes that are contextually aware. The tab completion is eerily accurate, often predicting exactly what you need. It supports multiple AI models under the hood (Claude, GPT) and lets you switch between them. For professional developers, it's become an essential tool — roughly 85% of developers now use some form of AI coding tool.",
        "pros": ["Full codebase understanding and context", "Agent mode handles complex multi-file changes", "Built on VS Code — familiar interface", "Tab completion is remarkably accurate", "Supports multiple underlying AI models"],
        "cons": ["$20/mo for Pro (required for serious use)", "Can be resource-intensive on older machines", "Occasional hallucinations in agent mode", "Learning curve for agent mode best practices"],
        "best_for_sections": "Cursor is the top choice for professional developers building real software — especially full-stack projects, refactoring legacy code, and anyone who wants AI deeply integrated into their coding workflow rather than as a separate chat window.",
        "competitors": [("windsurf", "Windsurf"), ("claude_code", "Claude Code")],
        "compare_link": "/compare/cursor-vs-windsurf.html"
    },
    "midjourney": {
        "name": "Midjourney",
        "version": "v7",
        "company": "Midjourney",
        "url": "https://midjourney.com",
        "pricing": "$10/mo (Basic) / $30/mo (Standard) / $60/mo (Pro)",
        "context": "Image generation",
        "bestFor": "Art, Creative visuals, Concept art, Campaigns",
        "title": "Midjourney v7 Review 2026 — Best AI Image Generator for Creatives",
        "meta_desc": "Midjourney v7 review for 2026. Now with web app, no Discord required. Still produces the most artistic AI images. Pricing, alternatives, and comparisons.",
        "meta_keywords": "Midjourney review, Midjourney v7, best AI image generator, Midjourney vs DALL-E, AI art generator 2026",
        "intro": "Midjourney pioneered AI image generation and continues to produce the most artistically stunning outputs in the space. Version 7 brings a proper web app (no more Discord-only access), improved prompt adherence, and better control over results.",
        "details": "While competitors have caught up in technical quality, Midjourney still has an unmistakable aesthetic quality that makes its outputs feel more \"designed\" than generated. The web app finally makes it accessible to non-Discord users. Personalization features let you train it on your preferred styles, and character reference tools help maintain consistency across images. The Basic plan at $10/mo gives you about 200 images — enough for most casual users. Note: free trials are currently suspended.",
        "pros": ["Most artistically beautiful outputs", "Web app now available (no Discord required)", "Style personalization and character references", "Strong community and prompt sharing", "Commercial usage rights included"],
        "cons": ["No free tier or trial currently available", "Less precise prompt adherence than some competitors", "Images are public by default on Basic plan", "No built-in image editing tools"],
        "best_for_sections": "Midjourney remains the top choice for creatives who prioritize aesthetic quality: concept artists, marketing teams needing campaign visuals, designers creating mood boards, and anyone where the artistic quality of the output matters more than pixel-perfect prompt adherence.",
        "competitors": [("ideogram", "Ideogram"), ("leonardo", "Leonardo AI")],
        "compare_link": "/compare/midjourney-vs-dalle.html"
    },
    "deepseek": {
        "name": "DeepSeek",
        "version": "V3.2",
        "company": "DeepSeek",
        "url": "https://chat.deepseek.com",
        "pricing": "Free chat / API from $0.07/M tokens",
        "context": "128K tokens",
        "bestFor": "Budget AI, Open source, Coding, API usage",
        "title": "DeepSeek V3.2 Review 2026 — Best Budget AI Model",
        "meta_desc": "DeepSeek V3.2 review for 2026. Open-source model with API costs as low as $0.07/M tokens. Competes with top models at a fraction of the cost.",
        "meta_keywords": "DeepSeek review, DeepSeek V3.2, cheapest AI API, open source AI, DeepSeek vs ChatGPT, budget AI model",
        "intro": "DeepSeek has disrupted the AI landscape by proving that world-class performance doesn't require world-class pricing. V3.2 features a novel Fine-Grained Sparse Attention architecture that improves efficiency by 50%, with API costs as low as $0.07 per million tokens.",
        "details": "DeepSeek V3.2 competes with models costing 10-100x more. It ranks in the top 10 on most major benchmarks including QA, reasoning, and agentic tasks. The open-weight model means you can self-host it for complete control and privacy. The free chat interface at chat.deepseek.com is fully functional for everyday use. For developers, the API pricing makes it viable for high-volume applications that would be cost-prohibitive with OpenAI or Anthropic. The main tradeoffs are higher latency compared to US-hosted models and some concerns about data routing through Chinese servers.",
        "pros": ["Extremely low API costs ($0.07-0.27/M tokens)", "Open weights — self-host for privacy", "Strong performance on coding benchmarks", "Free chat interface for personal use", "50% efficiency improvement with sparse attention"],
        "cons": ["Higher latency than US-hosted competitors", "Data privacy concerns (Chinese company)", "Smaller ecosystem and community", "Less polished conversational experience"],
        "best_for_sections": "DeepSeek is the best choice for developers building high-volume AI applications on a budget, self-hosting enthusiasts who want top performance locally, and anyone who needs strong AI capabilities without a $20/mo subscription.",
        "competitors": [("chatgpt", "ChatGPT"), ("mistral", "Mistral")],
        "compare_link": ""
    },
    "sora": {
        "name": "Sora",
        "version": "2",
        "company": "OpenAI",
        "url": "https://sora.com",
        "pricing": "Included with ChatGPT Plus ($20/mo)",
        "context": "Video generation",
        "bestFor": "Text-to-video, Product demos, Creative content",
        "title": "Sora 2 Review 2026 — OpenAI's Video Generation Model",
        "meta_desc": "Sora 2 review for 2026. OpenAI's text-to-video model included with ChatGPT Plus. Create cinematic videos from text prompts. Features, limitations, comparisons.",
        "meta_keywords": "Sora review, Sora 2 OpenAI, AI video generator, text to video AI, Sora vs Kling, best AI video",
        "intro": "Sora 2 brings cinematic-quality video generation to ChatGPT subscribers. Describe what you want to see, and Sora creates short video clips that are often indistinguishable from professionally shot footage.",
        "details": "Included with ChatGPT Plus at no extra cost, Sora 2 generates videos from text prompts, images, or existing video clips. The quality is remarkable for short-form content — product demos, social media clips, and creative concepts. It handles camera movement, lighting, and physics reasonably well. Limitations include video length (currently short clips), occasional physics errors, and difficulty with complex multi-character scenes. For professional video production it's a concept tool, not a replacement, but for social media and quick content it's genuinely useful.",
        "pros": ["Cinematic quality for short clips", "Included free with ChatGPT Plus subscription", "Text, image, and video-to-video generation", "Good physics and lighting understanding", "Integrated into ChatGPT ecosystem"],
        "cons": ["Limited to short video clips", "Occasional physics and anatomy errors", "Not suitable for long-form video production", "Can struggle with complex multi-person scenes"],
        "best_for_sections": "Sora is ideal for social media content creators, marketing teams creating quick product demos, creative concept visualization, and anyone who needs video content but doesn't have production resources.",
        "competitors": [("kling", "Kling AI")],
        "compare_link": ""
    },
    "ollama": {
        "name": "Ollama",
        "version": "Latest",
        "company": "Ollama",
        "url": "https://ollama.com",
        "pricing": "Free (open source)",
        "context": "Model dependent",
        "bestFor": "Local AI, Privacy, Offline use, Self-hosting",
        "title": "Ollama Review 2026 — Run AI Models Locally for Free",
        "meta_desc": "Ollama review for 2026. Run Llama, DeepSeek, Mistral, and 100+ AI models locally on your own hardware. Complete privacy, zero cost, offline access.",
        "meta_keywords": "Ollama review, run AI locally, local AI models, private AI, offline AI, self-hosted AI, Ollama tutorial",
        "intro": "Ollama lets you run powerful AI models on your own computer with zero cloud dependency. No subscriptions, no data leaving your machine, no internet required. It's the privacy-first choice for anyone handling sensitive information.",
        "details": "Ollama supports a growing library of models: Llama 4, DeepSeek V3.2, Mistral, Phi, Gemma, and many more. Installation is simple (one command), and switching between models takes seconds. Performance depends on your hardware — a modern laptop with 16GB+ RAM can run smaller models comfortably, while larger models benefit from dedicated GPUs. The trade-off is clear: you get complete privacy and zero cost, but the models you can run locally are generally smaller and less capable than cloud-hosted versions of GPT-5.2 or Claude Opus.",
        "pros": ["100% private — no data leaves your machine", "Completely free with no limits", "Works offline — no internet needed", "Supports 100+ models (Llama, DeepSeek, Mistral...)", "Simple installation and model switching"],
        "cons": ["Requires decent hardware for good performance", "Local models lag behind cloud frontier models", "No web search or real-time data", "Setup more technical than cloud alternatives"],
        "best_for_sections": "Ollama is the clear choice for handling sensitive data (medical, legal, financial), privacy-conscious users, developers building local AI applications, and anyone in environments without reliable internet access.",
        "competitors": [("deepseek", "DeepSeek"), ("mistral", "Mistral")],
        "compare_link": ""
    }
}

# ═══════════════ MODEL PAGE TEMPLATE ═══════════════
def generate_model_page(slug, data):
    competitors_html = ""
    for comp_slug, comp_name in data["competitors"]:
        competitors_html += f'''
    <a href="/models/{comp_slug}.html" class="nav-card">
      <div class="nav-card-label">Compare with</div>
      <div class="nav-card-name">{comp_name} →</div>
    </a>'''
    
    pros_html = "\n".join(f"      <li>{p}</li>" for p in data["pros"])
    cons_html = "\n".join(f"      <li>{c}</li>" for c in data["cons"])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{data["title"]} | SVPERFVTVRE</title>
  <meta name="description" content="{data["meta_desc"]}">
  <meta name="keywords" content="{data["meta_keywords"]}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://svperfvtvre.com/models/{slug}.html">
  <meta property="og:title" content="{data["title"]}">
  <meta property="og:description" content="{data["meta_desc"]}">
  <meta property="og:url" content="https://svperfvtvre.com/models/{slug}.html">
  <meta property="og:type" content="article">
  {FONTS_LINK}
  <style>{SHARED_CSS}</style>
</head>
<body>
  <header class="site-header"><div class="container"><a href="/" class="logo" style="text-decoration:none;">SVPERFVTVRE</a></div></header>
  <div class="container">
    <div class="breadcrumb"><a href="/">Home</a> / <a href="/models/">Models</a> / {data["name"]}</div>
    
    <h1>{data["name"]} {data["version"]}</h1>
    <div class="company">by {data["company"]}</div>
    <div class="version-badge">{data["version"]}</div>
    
    <p>{data["intro"]}</p>

    <div class="specs-grid">
      <div class="spec-card"><div class="spec-label">Pricing</div><div class="spec-value">{data["pricing"]}</div></div>
      <div class="spec-card"><div class="spec-label">Context Window</div><div class="spec-value">{data["context"]}</div></div>
      <div class="spec-card"><div class="spec-label">Best For</div><div class="spec-value">{data["bestFor"]}</div></div>
    </div>

    <h2>What's New in 2026</h2>
    <p>{data["details"]}</p>

    <h2>Strengths & Weaknesses</h2>
    <div class="pros-cons">
      <div class="pros">
        <h3>Pros</h3>
        <ul>
{pros_html}
        </ul>
      </div>
      <div class="cons">
        <h3>Cons</h3>
        <ul>
{cons_html}
        </ul>
      </div>
    </div>

    <h2>Best Use Cases</h2>
    <p>{data["best_for_sections"]}</p>

    <div class="cta-section">
      <p style="margin-bottom:1rem;">Ready to try {data["name"]}?</p>
      <a href="{data["url"]}" target="_blank" rel="noopener" class="cta-btn">Try {data["name"]} →</a>
      <p style="margin-top:1rem;font-size:0.8rem;color:var(--text-muted);">Or <a href="/">use our recommendation engine</a> to find the best model for your specific task.</p>
    </div>

    <h2>Compare {data["name"]}</h2>
    <div class="nav-cards">{competitors_html}
    </div>
  </div>
  <footer class="site-footer"><span>© 2026 SVPERFVTVRE</span> <a href="/">Home</a> <a href="/models/">All Models</a> <a href="/faq.html">FAQ</a></footer>
  <script defer src="/_vercel/insights/script.js"></script>
</body>
</html>'''


# ═══════════════ MODELS INDEX PAGE ═══════════════
def generate_models_index():
    cards = ""
    for slug, data in MODELS.items():
        cards += f'''
    <a href="/models/{slug}.html" class="nav-card" style="text-decoration:none;">
      <div class="nav-card-label">{data["company"]}</div>
      <div class="nav-card-name">{data["name"]} {data["version"]}</div>
      <div style="font-size:0.75rem;color:var(--text-muted);margin-top:0.3rem;">{data["bestFor"]}</div>
    </a>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>All AI Models Compared — 2026 Rankings | SVPERFVTVRE</title>
  <meta name="description" content="Compare 25+ AI models side-by-side. GPT-5.2, Claude Opus 4.5, Gemini 3 Pro, Grok 4.1, Midjourney, Cursor, and more. Updated February 2026.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://svperfvtvre.com/models/">
  {FONTS_LINK}
  <style>{SHARED_CSS}
  .models-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1rem; margin: 2rem 0; }}
  </style>
</head>
<body>
  <header class="site-header"><div class="container"><a href="/" class="logo" style="text-decoration:none;">SVPERFVTVRE</a></div></header>
  <div class="container">
    <div class="breadcrumb"><a href="/">Home</a> / Models</div>
    <h1>All AI Models</h1>
    <p>Every model in our recommendation engine, reviewed and compared. Updated February 2026.</p>
    <div class="models-grid">{cards}
    </div>
    <div class="cta-section">
      <p style="margin-bottom:1rem;">Not sure which model is right for you?</p>
      <a href="/" class="cta-btn">Use our recommendation engine →</a>
    </div>
  </div>
  <footer class="site-footer"><span>© 2026 SVPERFVTVRE</span> <a href="/">Home</a> <a href="/faq.html">FAQ</a></footer>
  <script defer src="/_vercel/insights/script.js"></script>
</body>
</html>'''


# ═══════════════ COMPARISON PAGES ═══════════════
COMPARISONS = {
    "claude-vs-chatgpt": {
        "title": "Claude vs ChatGPT in 2026 — Which AI Is Better?",
        "meta_desc": "Claude Opus 4.5 vs ChatGPT GPT-5.2: detailed comparison of features, pricing, coding, writing, and more. Updated February 2026.",
        "meta_keywords": "Claude vs ChatGPT, Claude vs GPT-5, best AI 2026, Claude or ChatGPT, AI comparison",
        "model_a": "Claude Opus 4.5",
        "model_b": "ChatGPT GPT-5.2",
        "intro": "The two most popular AI assistants go head-to-head. Claude Opus 4.5 from Anthropic and ChatGPT's GPT-5.2 from OpenAI are both flagship models, but they excel in different areas.",
        "rows": [
            ("Company", "Anthropic", "OpenAI", ""),
            ("Pricing", "$20/mo (Pro)", "$20/mo (Plus) / $8/mo (Go)", "b"),
            ("Context Window", "200K tokens", "400K tokens", "b"),
            ("Writing Quality", "Exceptional — nuanced, follows complex instructions", "Very good — can be verbose", "a"),
            ("Coding", "Top-tier via Claude Code CLI + chat", "Strong — GPT-5.2 Codex leads benchmarks", "tie"),
            ("Math & Reasoning", "Strong but not #1", "Perfect AIME 2025 score", "b"),
            ("Image Generation", "Not available natively", "Built-in (GPT-4o + DALL-E)", "b"),
            ("Video Generation", "Not available", "Sora 2 included", "b"),
            ("Web Search", "Via tools", "Built-in browsing", "b"),
            ("Hallucination Rate", "Low — known for careful responses", "6.2% (40% reduction)", "a"),
            ("Ecosystem", "Growing — Claude Code, API", "Massive — GPTs, plugins, integrations", "b"),
            ("Free Tier", "Limited but functional", "Limited but functional", "tie"),
            ("Open Source", "No", "Yes — GPT-oss models (Apache 2.0)", "b"),
        ],
        "verdict_title": "The Verdict",
        "verdict": "Choose Claude if you prioritize writing quality, instruction-following, and coding via Claude Code. Choose ChatGPT if you want the most versatile all-in-one tool with image generation, video, web browsing, and the largest ecosystem. For most users, ChatGPT's breadth wins; for professionals who need precision, Claude's depth wins.",
        "link_a": "/models/claude.html",
        "link_b": "/models/chatgpt.html"
    },
    "cursor-vs-windsurf": {
        "title": "Cursor vs Windsurf in 2026 — Best AI Code Editor",
        "meta_desc": "Cursor vs Windsurf (Codeium): detailed comparison of AI coding IDEs. Agent mode, pricing, performance, and which to choose. Updated February 2026.",
        "meta_keywords": "Cursor vs Windsurf, best AI IDE, Cursor vs Codeium, AI code editor comparison, best AI for coding",
        "model_a": "Cursor",
        "model_b": "Windsurf (Codeium)",
        "intro": "The two leading AI-native code editors battle for developers' attention. Both are built on VS Code and offer agentic coding capabilities, but they differ in pricing, performance, and approach.",
        "rows": [
            ("Company", "Cursor", "Codeium", ""),
            ("Base", "VS Code fork", "VS Code fork", "tie"),
            ("Pricing", "$20/mo Pro / $40/mo Business", "$15/mo Pro", "b"),
            ("Free Tier", "Limited", "Generous", "b"),
            ("Agent Mode", "Mature, multi-file refactors", "Growing, solid for simpler tasks", "a"),
            ("Tab Completion", "Excellent — eerily accurate", "Very good", "a"),
            ("Codebase Understanding", "Deep — reads entire project", "Good — improving", "a"),
            ("Speed", "Can be resource-heavy", "Generally lighter", "b"),
            ("Model Support", "Claude, GPT (switchable)", "Multiple models", "tie"),
            ("Enterprise Features", "Team management, SSO", "Team features available", "tie"),
        ],
        "verdict_title": "The Verdict",
        "verdict": "Cursor is the better tool for professional developers working on complex projects where agent mode and codebase understanding matter. Windsurf is the better value if you want solid AI coding assistance at a lower price point. If budget matters, start with Windsurf; if capability matters, go with Cursor.",
        "link_a": "/models/cursor.html",
        "link_b": ""
    },
    "midjourney-vs-dalle": {
        "title": "Midjourney vs DALL-E vs ChatGPT Image in 2026",
        "meta_desc": "Midjourney v7 vs ChatGPT Image (GPT-4o) vs Ideogram: which AI image generator is best? Quality, pricing, features compared. February 2026.",
        "meta_keywords": "Midjourney vs DALL-E, best AI image generator, Midjourney vs ChatGPT image, AI art comparison 2026",
        "model_a": "Midjourney v7",
        "model_b": "ChatGPT Image (GPT-4o)",
        "intro": "AI image generation has exploded with options. Midjourney still leads in artistic quality, but ChatGPT's built-in image generation (which replaced standalone DALL-E) and newcomers like Ideogram have changed the landscape.",
        "rows": [
            ("Company", "Midjourney", "OpenAI", ""),
            ("Pricing", "$10-60/mo", "Included with ChatGPT ($20/mo)", "b"),
            ("Artistic Quality", "Best-in-class — stunning aesthetics", "Very good — improving rapidly", "a"),
            ("Prompt Adherence", "Good but sometimes loose", "Strong — follows instructions well", "b"),
            ("Text in Images", "Weak", "Moderate", "tie"),
            ("Editing / Iteration", "Limited — re-roll or vary", "Conversational editing", "b"),
            ("Style Consistency", "Personalization + character refs", "Limited", "a"),
            ("Free Tier", "None (trials suspended)", "Limited free with ChatGPT", "b"),
            ("Interface", "Web app + Discord", "Chat interface", "b"),
            ("Commercial Rights", "Included in all paid plans", "Included", "tie"),
            ("Speed", "Fast", "Fast", "tie"),
        ],
        "verdict_title": "The Verdict",
        "verdict": "Choose Midjourney if aesthetics are your top priority — concept art, campaign visuals, mood boards. Choose ChatGPT Image if you want image gen as part of an all-in-one tool and prefer conversational editing. Choose Ideogram if you need text rendering in images (logos, posters, banners). Choose Leonardo AI if you need multiple models and a canvas editor.",
        "link_a": "/models/midjourney.html",
        "link_b": "/models/chatgpt.html"
    }
}


def generate_comparison_page(slug, data):
    rows_html = ""
    for label, val_a, val_b, winner in data["rows"]:
        class_a = ' class="winner"' if winner == "a" else ""
        class_b = ' class="winner"' if winner == "b" else ""
        rows_html += f"      <tr><td>{label}</td><td{class_a}>{val_a}</td><td{class_b}>{val_b}</td></tr>\n"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{data["title"]} | SVPERFVTVRE</title>
  <meta name="description" content="{data["meta_desc"]}">
  <meta name="keywords" content="{data["meta_keywords"]}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://svperfvtvre.com/compare/{slug}.html">
  <meta property="og:title" content="{data["title"]}">
  <meta property="og:description" content="{data["meta_desc"]}">
  {FONTS_LINK}
  <style>{SHARED_CSS}</style>
</head>
<body>
  <header class="site-header"><div class="container"><a href="/" class="logo" style="text-decoration:none;">SVPERFVTVRE</a></div></header>
  <div class="container">
    <div class="breadcrumb"><a href="/">Home</a> / <a href="/models/">Models</a> / {data["model_a"]} vs {data["model_b"]}</div>
    
    <h1>{data["model_a"]} vs {data["model_b"]}</h1>
    <p>{data["intro"]}</p>

    <h2>Side-by-Side Comparison</h2>
    <div style="overflow-x:auto;">
    <table class="compare-table">
      <thead><tr><th></th><th>{data["model_a"]}</th><th>{data["model_b"]}</th></tr></thead>
      <tbody>
{rows_html}      </tbody>
    </table>
    </div>

    <div class="verdict">
      <h3>{data["verdict_title"]}</h3>
      <p>{data["verdict"]}</p>
    </div>

    <div class="cta-section">
      <p style="margin-bottom:1rem;">Still not sure? Describe your task and we'll recommend the right model.</p>
      <a href="/" class="cta-btn">Try the recommendation engine →</a>
    </div>

    <div class="nav-cards">
      <a href="{data["link_a"]}" class="nav-card" style="text-decoration:none;">
        <div class="nav-card-label">Full review</div>
        <div class="nav-card-name">{data["model_a"]} →</div>
      </a>
      <a href="{data["link_b"] or '/models/'}" class="nav-card" style="text-decoration:none;">
        <div class="nav-card-label">Full review</div>
        <div class="nav-card-name">{data["model_b"]} →</div>
      </a>
    </div>
  </div>
  <footer class="site-footer"><span>© 2026 SVPERFVTVRE</span> <a href="/">Home</a> <a href="/models/">All Models</a> <a href="/faq.html">FAQ</a></footer>
  <script defer src="/_vercel/insights/script.js"></script>
</body>
</html>'''


# ═══════════════ GENERATE ALL FILES ═══════════════
if __name__ == "__main__":
    # Model profile pages
    models_dir = os.path.join(OUTPUT_DIR, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    for slug, data in MODELS.items():
        filepath = os.path.join(models_dir, f"{slug}.html")
        with open(filepath, "w") as f:
            f.write(generate_model_page(slug, data))
        print(f"✓ Generated models/{slug}.html")
    
    # Models index page
    filepath = os.path.join(models_dir, "index.html")
    with open(filepath, "w") as f:
        f.write(generate_models_index())
    print(f"✓ Generated models/index.html")
    
    # Comparison pages
    compare_dir = os.path.join(OUTPUT_DIR, "compare")
    os.makedirs(compare_dir, exist_ok=True)
    
    for slug, data in COMPARISONS.items():
        filepath = os.path.join(compare_dir, f"{slug}.html")
        with open(filepath, "w") as f:
            f.write(generate_comparison_page(slug, data))
        print(f"✓ Generated compare/{slug}.html")
    
    print(f"\n{'='*50}")
    print(f"Total: {len(MODELS)} model pages + 1 index + {len(COMPARISONS)} comparisons")
    print(f"{'='*50}")

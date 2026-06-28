

export const TrustedTech = () => {
  return (
    <section className="py-12 border-y border-white/5 bg-background">
      <div className="max-w-7xl mx-auto px-6">
        <p className="text-center text-sm text-muted-foreground mb-8">
          Built on enterprise-grade infrastructure
        </p>
        <div className="flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-60 grayscale hover:grayscale-0 transition-all duration-500">
          {/* Placeholders for logos */}
          <div className="flex items-center gap-2 font-semibold text-lg"><div className="w-6 h-6 rounded-full bg-current" /> AWS</div>
          <div className="flex items-center gap-2 font-semibold text-lg"><div className="w-6 h-6 rounded-sm bg-current" /> OpenAI</div>
          <div className="flex items-center gap-2 font-semibold text-lg"><div className="w-6 h-6 rounded-sm bg-current" /> Anthropic</div>
          <div className="flex items-center gap-2 font-semibold text-lg"><div className="w-6 h-6 rounded-sm bg-current" /> LangChain</div>
          <div className="flex items-center gap-2 font-semibold text-lg"><div className="w-6 h-6 rounded-sm bg-current" /> Vercel</div>
        </div>
      </div>
    </section>
  );
};

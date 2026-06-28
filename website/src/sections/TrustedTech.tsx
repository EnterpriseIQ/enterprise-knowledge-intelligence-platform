const logos = [
  { name: "AWS", path: "M11.96 15.65c-1.57.88-3.5 1.54-5.38 1.54-1.95 0-3.32-.96-3.32-2.58 0-1.8 1.6-2.58 3.73-2.94l2.18-.36v-.55c0-.98-.56-1.55-1.78-1.55-1.12 0-2.34.42-3.14.92l-.78-1.92c1.07-.63 2.73-1.07 4.28-1.07 2.76 0 4.14 1.34 4.14 3.75v5.82h-2.12v-1.08h.18c-.46.54-1.18 1.08-1.99 1.08v-.06zM9.9 12.6v-.72l-1.9.3c-1.12.18-1.63.54-1.63 1.25 0 .7.59 1.15 1.48 1.15 1.14.02 2.05-.62 2.05-1.98z" },
  { name: "OpenAI", path: "M22.28 10.43c-.48-2.61-2.4-4.52-5-5-1.22-3.13-4.98-4.53-8.22-3.08C6.67.6 3.65 1.94 2.22 4.41c-2.48 1-3.66 3.78-2.82 6.27-.48 2.61 1.44 5.25 4.05 5.75 1.22 3.13 4.98 4.53 8.22 3.08 2.39 1.75 5.41.41 6.84-2.06 2.48-1 3.66-3.78 2.82-6.27l-.05-.75zM11.16 2.37c2.25-.66 4.67.43 5.66 2.51-1.44.07-2.86.43-4.14 1.06L11 6.84V2.42c.05-.02.1-.04.16-.05z" },
  { name: "Anthropic", path: "M12 2L2 22h4.5l2.25-4.5h6.5L17.5 22H22L12 2zm0 5.5l2 4h-4l2-4z" },
  { name: "LangChain", path: "M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8zm4-8a4 4 0 1 1-8 0 4 4 0 0 1 8 0z" },
  { name: "Vercel", path: "M24 22.525H0l12-21.05 12 21.05z" }
];

export const TrustedTech = () => {
  return (
    <section className="py-12 border-y border-white/5 bg-background">
      <div className="max-w-7xl mx-auto px-6">
        <p className="text-center text-sm text-muted-foreground mb-8">
          Built on enterprise-grade infrastructure
        </p>
        <div className="flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-60 grayscale hover:grayscale-0 transition-all duration-500">
          {logos.map((logo) => (
            <div key={logo.name} className="flex items-center gap-2 font-semibold text-lg hover:text-white transition-colors cursor-default">
              <svg viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
                <path d={logo.path} />
              </svg>
              {logo.name}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

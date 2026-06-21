export const Footer = () => {
  return (
    <footer className="border-t border-white/10 bg-background pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16 text-sm">
          <div className="col-span-2 md:col-span-1">
            <a href="/" className="font-semibold text-lg tracking-tight flex items-center gap-2 mb-4">
              <div className="w-5 h-5 rounded-[4px] bg-white text-black flex items-center justify-center text-xs font-bold">K</div>
              Kortex
            </a>
            <p className="text-muted-foreground">
              The Intelligence Layer for Enterprise Knowledge.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-white mb-4">Product</h4>
            <ul className="space-y-3 text-muted-foreground">
              <li><a href="#features" className="hover:text-white transition-colors">Features</a></li>
              <li><a href="#architecture" className="hover:text-white transition-colors">Architecture</a></li>
              <li><a href="#security" className="hover:text-white transition-colors">Security</a></li>
              <li><a href="/pricing" className="hover:text-white transition-colors">Enterprise</a></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-white mb-4">Resources</h4>
            <ul className="space-y-3 text-muted-foreground">
              <li><a href="/docs" className="hover:text-white transition-colors">Documentation</a></li>
              <li><a href="/api" className="hover:text-white transition-colors">API Reference</a></li>
              <li><a href="https://github.com/your-repo/enterprise-rag-platform" className="hover:text-white transition-colors">GitHub</a></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-white mb-4">Company</h4>
            <ul className="space-y-3 text-muted-foreground">
              <li><a href="/about" className="hover:text-white transition-colors">About</a></li>
              <li><a href="/blog" className="hover:text-white transition-colors">Blog</a></li>
              <li><a href="/contact" className="hover:text-white transition-colors">Contact</a></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-white/10 pt-8 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-muted-foreground">
          <p>© {new Date().getFullYear()} Kortex Inc. All rights reserved.</p>
          <div className="flex gap-4">
            <a href="/privacy" className="hover:text-white transition-colors">Privacy Policy</a>
            <a href="/terms" className="hover:text-white transition-colors">Terms of Service</a>
            <a href="https://github.com/your-repo/enterprise-rag-platform" aria-label="GitHub repository" className="hover:text-white transition-colors">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="w-4 h-4"
              >
                <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
                <path d="M9 18c-4.51 2-5-2-7-2" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};
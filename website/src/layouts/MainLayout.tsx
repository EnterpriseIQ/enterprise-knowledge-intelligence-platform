import React from 'react';


export function MainLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background text-foreground selection:bg-primary selection:text-primary-foreground dark">
      <div className="relative flex min-h-screen flex-col">
        {/* Animated Background Gradients */}
        <div className="pointer-events-none fixed inset-0 z-0 flex justify-center overflow-hidden">
          <div className="absolute left-[50%] top-0 h-[600px] w-[600px] -translate-x-[50%] translate-y-[-20%] rounded-full bg-primary/20 opacity-50 blur-[120px]" />
          <div className="absolute left-[20%] top-[40%] h-[400px] w-[400px] rounded-full bg-secondary/10 opacity-30 blur-[100px]" />
        </div>

        {/* Main Content Area */}
        <main className="flex-1 relative z-10 w-full overflow-hidden">
          {children}
        </main>
      </div>
    </div>
  );
}

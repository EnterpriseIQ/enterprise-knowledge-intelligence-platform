import { Hero } from '../sections/Hero';
import { Navigation } from '../sections/Navigation';
import { TrustedTech } from '../sections/TrustedTech';
import { Problem } from '../sections/Problem';
import { Solution } from '../sections/Solution';
import { Features } from '../sections/Features';
import { Architecture } from '../sections/Architecture';
import { HowItWorks } from '../sections/HowItWorks';
import { Demo } from '../sections/Demo';
import { Performance } from '../sections/Performance';
import { Security } from '../sections/Security';
import { EnterpriseFeatures } from '../sections/EnterpriseFeatures';
import { DevExperience } from '../sections/DevExperience';
import { Documentation } from '../sections/Documentation';
import { Roadmap } from '../sections/Roadmap';
import { FAQ } from '../sections/FAQ';
import { CTA } from '../sections/CTA';
import { Footer } from '../sections/Footer';

export const Home = () => {
  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <Navigation />
      <main className="flex-1 flex flex-col w-full">
        <Hero />
        <TrustedTech />
        <Problem />
        <Solution />
        <Features />
        <Architecture />
        <HowItWorks />
        <Demo />
        <Performance />
        <Security />
        <EnterpriseFeatures />
        <DevExperience />
        <Documentation />
        <Roadmap />
        <FAQ />
        <CTA />
      </main>
      <Footer />
    </div>
  );
};

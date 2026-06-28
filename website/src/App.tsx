
import { MainLayout } from './layouts/MainLayout';
import { Navigation } from './sections/Navigation';
import { Hero } from './sections/Hero';
import { TrustedTech } from './sections/TrustedTech';
import { ProblemSolution } from './sections/ProblemSolution';
import { Demo } from './sections/Demo';
import { Features } from './sections/Features';
import { Architecture } from './sections/Architecture';
import { DeveloperExperience } from './sections/DeveloperExperience';
import { FaqCta } from './sections/FaqCta';
import { Footer } from './sections/Footer';

function App() {
  return (
    <MainLayout>
      <Navigation />
      <Hero />
      <TrustedTech />
      <ProblemSolution />
      <Demo />
      <Features />
      <Architecture />
      <DeveloperExperience />
      <FaqCta />
      <Footer />
    </MainLayout>
  );
}

export default App;

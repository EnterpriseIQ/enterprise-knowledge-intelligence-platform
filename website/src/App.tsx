
import { MainLayout } from './layouts/MainLayout';
import { Navigation } from './sections/Navigation';
import { Hero } from './sections/Hero';
import { TrustedBy } from './sections/TrustedBy';
import { ProblemSolution } from './sections/ProblemSolution';
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
      <TrustedBy />
      <ProblemSolution />
      <Features />
      <Architecture />
      <DeveloperExperience />
      <FaqCta />
      <Footer />
    </MainLayout>
  );
}

export default App;

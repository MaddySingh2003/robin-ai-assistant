import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';
import { tsParticles } from '@tsparticles/engine';
import { loadSlim } from '@tsparticles/slim';

// Initialize the tsParticles engine globally before bootstrapping the app
loadSlim(tsParticles).then(() => {
  bootstrapApplication(App, appConfig)
    .catch((err) => console.error(err));
});

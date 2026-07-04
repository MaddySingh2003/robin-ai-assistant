import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './navbar.component';
import { HeroComponent } from './hero.component';
import { ParticlesComponent } from './particles.component';
import { FeaturesComponent } from './features.component';
import { InstallationComponent } from './installation.component';
import { RoadmapComponent } from './roadmap.component';
import { FooterComponent } from './footer.component';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    NavbarComponent,
    HeroComponent,
    ParticlesComponent,
    FeaturesComponent,
    InstallationComponent,
    RoadmapComponent,
    FooterComponent
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  readonly title = 'ROBIN AI Assistant';
}

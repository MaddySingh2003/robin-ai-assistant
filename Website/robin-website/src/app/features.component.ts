import { Component, signal } from '@angular/core';

interface FeatureCard {
  icon: string;
  title: string;
  description: string;
  badge: string;
  gradient: string;
}

@Component({
  selector: 'app-features',
  standalone: true,
  imports: [],
  templateUrl: './features.component.html',
  styleUrls: ['./features.component.css']
})
export class FeaturesComponent {
  features = signal<FeatureCard[]>([
    {
      icon: '🎙️',
      title: 'Voice Interaction',
      description: 'Interact with Robin naturally using speech. It converts voice input, queries local models, and speaks back to you.',
      badge: 'Interactive',
      gradient: 'var(--grad-cyan-violet)'
    },
    {
      icon: '🧠',
      title: 'Vector Memory System',
      description: 'Built-in semantic memory remembers past interactions, projects, and context, allowing Robin to recall details across restarts.',
      badge: 'Local DB',
      gradient: 'var(--grad-violet-pink)'
    },
    {
      icon: '🤖',
      title: 'Autonomous Planning',
      description: 'Give Robin a goal, and its PlannerAgent breaks it down into sequential tasks and executes them step-by-step.',
      badge: 'Agentic',
      gradient: 'var(--grad-gold-orange)'
    },
    {
      icon: '💻',
      title: 'Project Generation',
      description: 'Generates entire codebases, file trees, scripts, or documentation using robust local generation templates.',
      badge: 'Automation',
      gradient: 'var(--grad-cyan-violet)'
    },
    {
      icon: '⚙️',
      title: 'Command Execution',
      description: 'Executes scripts, system diagnostics, or workspace commands locally with integrated permission reviews.',
      badge: 'System Integration',
      gradient: 'var(--grad-violet-pink)'
    },
    {
      icon: '🔒',
      title: '100% Local-First',
      description: 'Keeps all code, logs, vector databases, and memory completely local to ensure maximum privacy and security.',
      badge: 'Privacy',
      gradient: 'var(--grad-gold-orange)'
    }
  ]);
}

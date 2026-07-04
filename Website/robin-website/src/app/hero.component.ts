import { Component, signal, OnInit, OnDestroy } from '@angular/core';

interface TerminalLine {
  text: string;
  type: 'input' | 'system' | 'success' | 'info';
}

@Component({
  selector: 'app-hero',
  standalone: true,
  imports: [],
  templateUrl: './hero.component.html',
  styleUrls: ['./hero.component.css']
})
export class HeroComponent implements OnInit, OnDestroy {
  readonly heading = signal('ROBIN');
  readonly subheading = signal('The Autonomous AI Desktop Assistant');
  readonly description = signal('A local, modular AI agent capable of voice interaction, memory management, tool execution, and project generation.');

  // Terminal Simulation
  terminalLines = signal<TerminalLine[]>([]);
  terminalCursor = signal(true);
  private simulationInterval: any;
  private cursorInterval: any;

  ngOnInit(): void {
    this.startTerminalSimulation();
    this.startCursorBlink();
  }

  ngOnDestroy(): void {
    if (this.simulationInterval) clearInterval(this.simulationInterval);
    if (this.cursorInterval) clearInterval(this.cursorInterval);
  }

  private startCursorBlink(): void {
    this.cursorInterval = setInterval(() => {
      this.terminalCursor.update(v => !v);
    }, 500);
  }

  private startTerminalSimulation(): void {
    const simulationSteps = [
      { text: 'robin --voice-mode', type: 'input', delay: 1000 },
      { text: 'Initializing voice recognition engine...', type: 'system', delay: 1800 },
      { text: '🎙️ Voice Active: "Hey Robin, generate a NextJS dashboard and run the build."', type: 'info', delay: 3500 },
      { text: 'Executing PlannerAgent workflows...', type: 'system', delay: 4500 },
      { text: '✔ Created layout.tsx, page.tsx, and tailwind.config.js', type: 'success', delay: 6000 },
      { text: '⚙ Running system command: npm run build', type: 'info', delay: 7200 },
      { text: '✔ NextJS build complete! Local: http://localhost:3000', type: 'success', delay: 9000 },
      { text: '✨ Task complete. Memory synced locally.', type: 'system', delay: 11000 }
    ];

    let currentStep = 0;
    
    // Initial run
    this.runStep(simulationSteps[currentStep]);

    this.simulationInterval = setInterval(() => {
      currentStep++;
      if (currentStep >= simulationSteps.length) {
        currentStep = 0;
        this.terminalLines.set([]); // Clear terminal for loop
      }
      this.runStep(simulationSteps[currentStep]);
    }, 1800); // Trigger a new step periodically
  }

  private runStep(step: { text: string; type: string }): void {
    if (!step) return;
    this.terminalLines.update(lines => [
      ...lines,
      { text: step.text, type: step.type as any }
    ]);
  }
}

import { Component, signal } from '@angular/core';

interface RoadmapItem {
  phase: string;
  title: string;
  status: 'completed' | 'current' | 'future';
  description: string;
  points: string[];
}

@Component({
  selector: 'app-roadmap',
  standalone: true,
  imports: [],
  templateUrl: './roadmap.component.html',
  styleUrls: ['./roadmap.component.css']
})
export class RoadmapComponent {
  roadmapItems = signal<RoadmapItem[]>([
    {
      phase: 'Phase 1',
      title: 'Speech Recognition & Adaptation',
      status: 'completed',
      description: 'Laying down the core real-time communication stack for speech input and playback output.',
      points: [
        'Voice threshold activation with PyAudio',
        'Offline Whisper transcription integrations',
        'Text-to-speech feedback (pyttsx3 & OpenAI TTS)',
        'Local console debugging panel setup'
      ]
    },
    {
      phase: 'Phase 2',
      title: 'Semantic Memory Integrations',
      status: 'completed',
      description: 'Integrating a permanent memory module allowing Robin to maintain contextual data between sessions.',
      points: [
        'Local vector database setup using ChromaDB',
        'Automatic embedding storage of system interaction logs',
        'Keyword and context retrieval queries',
        'Dynamic configuration memory profile management'
      ]
    },
    {
      phase: 'Phase 3',
      title: 'Agent Planning & Toolkits',
      status: 'completed',
      description: 'Evolving the agent from basic command execution to multi-step reasoning models.',
      points: [
        'Chain-of-thought planning structures (PlannerAgent)',
        'Local file utilities (read/write/scan system workspace)',
        'Process and terminal command triggers with security verification',
        'Error diagnostics and self-healing loop implementation'
      ]
    },
    {
      phase: 'Phase 4',
      title: 'Orchestration & Window Overlays',
      status: 'current',
      description: 'Developing multi-agent task division and a clean, responsive UI wrapper for standard desktop use.',
      points: [
        'Dynamic sub-agent spawning (Coder, Analyst, Searcher)',
        'Interactive window overlay displaying agent logic tree',
        'Semantic file search indexes',
        'Integrated browser automation module'
      ]
    }
  ]);
}

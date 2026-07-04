import { Component, signal } from '@angular/core';

interface Step {
  title: string;
  command: string;
  comment: string;
}

@Component({
  selector: 'app-installation',
  standalone: true,
  imports: [],
  templateUrl: './installation.component.html',
  styleUrls: ['./installation.component.css']
})
export class InstallationComponent {
  activeTab = signal<'local' | 'env'>('local');

  localSteps = signal<Step[]>([
    {
      title: 'Clone Project Repository',
      command: 'git clone https://github.com/MaddySingh2003/robin-ai-assistant.git\ncd robin-ai-assistant',
      comment: '# Fetch the repository and enter directory'
    },
    {
      title: 'Setup Virtual Environment',
      command: 'python -m venv venv\n.\\venv\\Scripts\\activate',
      comment: '# Create and activate environment (Windows)'
    },
    {
      title: 'Install Required Dependencies',
      command: 'pip install -r requirements.txt',
      comment: '# Installs core requirements, LLM adapters, ChromaDB'
    },
    {
      title: 'Initialize & Run Robin',
      command: 'python main.py',
      comment: '# Launches voice, planning system, and agent shell'
    }
  ]);

  envConfigs = signal<{ key: string; value: string; desc: string }[]>([
    { key: 'OPENAI_API_KEY', value: 'sk-...', desc: 'Your OpenAI API key (if using GPT-4o/GPT-3.5)' },
    { key: 'OLLAMA_HOST', value: 'http://localhost:11434', desc: 'Ollama local host (for fully offline local run)' },
    { key: 'VOICE_PROVIDER', value: 'openai | local', desc: 'Configure voice transcription/TTS provider' },
    { key: 'MEMORY_DIR', value: './memory_db', desc: 'Custom local ChromaDB persistence path' }
  ]);

  copied = signal<number | null>(null);

  setTab(tab: 'local' | 'env'): void {
    this.activeTab.set(tab);
  }

  copyToClipboard(text: string, index: number): void {
    navigator.clipboard.writeText(text).then(() => {
      this.copied.set(index);
      setTimeout(() => this.copied.set(null), 2000);
    });
  }
}

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common'; // For common directives
import { TextToSpeechComponent } from './text-to-speech/text-to-speech.component'; // Import your component

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, TextToSpeechComponent], // Import standalone components/directives
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Text to Speech App';
}
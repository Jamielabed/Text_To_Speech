import { Component } from '@angular/core';
import { CommonModule } from '@angular/common'; // For common directives
import { FormsModule } from '@angular/forms'; // For template-driven forms
import { ApiService } from '../api.service';

@Component({
  selector: 'app-text-to-speech',
  standalone: true,
  imports: [CommonModule, FormsModule], // Import standalone components/directives
  templateUrl: './text-to-speech.component.html',
  styleUrls: ['./text-to-speech.component.css']
})
export class TextToSpeechComponent {
  selectedFile: File | null = null;
  audioUrl: string | null = null; // Store the audio file URL

  constructor(private apiService: ApiService) {}

  // Handle file selection via input
  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
    this.audioUrl = null; // Reset the audio URL when a new file is selected
  }

  // Convert the file to speech
  convertTextToSpeech() {
    if (!this.selectedFile) {
      alert('Please select a file.');
      return;
    }

    this.apiService.textToSpeech(this.selectedFile).subscribe(
      (response: Blob) => {
        // Create a URL for the audio file
        this.audioUrl = window.URL.createObjectURL(response);
      },
      (error) => {
        console.error('Error converting text to speech:', error);
        alert('An error occurred while converting the file. Please try again.');
      }
    );
  }
}
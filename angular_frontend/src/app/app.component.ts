import {
  ChangeDetectorRef,
  Component,
  ElementRef,
  ViewChild,
  inject,
} from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HlmButtonDirective } from '@spartan-ng/ui-button-helm';
import {
  HlmCardContentDirective,
  HlmCardDescriptionDirective,
  HlmCardDirective,
  HlmCardFooterDirective,
  HlmCardHeaderDirective,
  HlmCardTitleDirective,
} from '@spartan-ng/ui-card-helm';
import { HlmInputDirective } from '@spartan-ng/ui-input-helm';
import { SvgPipe } from './shared/pipes/svg.pipe';
import { AppService } from './shared/services/app.service';
import { NgClass } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    FormsModule,
    HlmCardDirective,
    HlmCardHeaderDirective,
    HlmCardTitleDirective,
    HlmCardDescriptionDirective,
    HlmCardContentDirective,
    HlmInputDirective,
    HlmCardFooterDirective,
    HlmButtonDirective,
    SvgPipe,
    NgClass,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  private cd = inject(ChangeDetectorRef);

  @ViewChild('slider') slider!: ElementRef<HTMLDivElement>;
  @ViewChild('afterImage') afterImage!: ElementRef<HTMLImageElement>;

  sliderPosition: number = 50;
  isPreviewDragging: boolean = false;
  selectedFile: File | null = null;
  isDragging: boolean = false;
  ngrokUrl: string | null = null;
  githubProfiles: any[] = [];
  isImageLoading: boolean = false;
  isUploadPage: boolean = true;
  isLiked: boolean = false;
  isDisliked: boolean = false;
  beforeImageUrl: string = '';
  afterImageUrl: string = '';

  private appService = inject(AppService);

  ngOnInit(): void {
    document.documentElement.classList.toggle('dark');
    this.loadGithubProfiles(['Deepchavda007', 'Jaydip-Hadiya']);
  }

  ngAfterViewInit(): void {
    this.updateClipPath();
  }

  // Method to fetch GitHub profiles
  loadGithubProfiles(usernames: string[]): void {
    usernames.forEach((username) => {
      this.appService.getGithubProfile(username).subscribe((profile) => {
        this.githubProfiles.push(profile);
      });
    });
  }

  // Trigger file input for image upload
  triggerFileInput(fileInput: HTMLInputElement): void {
    fileInput.click();
  }

  // Handle file input change event
  onFileChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input?.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      this.uploadImage();
    }
  }

  // Handle image upload process
  uploadImage(): void {
    if (this.selectedFile) {
      this.isUploadPage = false;
      this.isImageLoading = true;

      const formData = new FormData();
      formData.append('image', this.selectedFile);

      this.appService.uploadImage(formData).subscribe({
        next: (response) => {
          this.handleImageUploadSuccess(response);
        },
        error: (err) => {
          console.error('Image upload failed:', err);
        },
      });
    }
  }

  private handleImageUploadSuccess(response: any): void {
    this.afterImageUrl = response.filePath;
    this.beforeImageUrl = response.removeBgApiResponse.data.remove_bg_url;
    this.isImageLoading = false;

    // Wait until afterImage is rendered and available in the DOM
    this.cd.detectChanges();
    this.updateClipPath();
  }

  // Drag and drop events for image upload
  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = false;
    if (event.dataTransfer && event.dataTransfer.files.length > 0) {
      this.selectedFile = event.dataTransfer.files[0];
      this.uploadImage();
    }
  }

  // Handle mouse events for slider movement
  onMouseDown(event: MouseEvent): void {
    this.isPreviewDragging = true;
    this.updateSliderPosition(event);
  }

  onMouseMove(event: MouseEvent): void {
    if (this.isPreviewDragging) {
      this.updateSliderPosition(event);
    }
  }

  onMouseUp(): void {
    this.isPreviewDragging = false;
  }

  // Adjust slider based on mouse movement
  private updateSliderPosition(event: MouseEvent): void {
    const sliderRect = this.slider.nativeElement.getBoundingClientRect();
    const newPosition =
      ((event.clientX - sliderRect.left) / sliderRect.width) * 100;
    this.sliderPosition = Math.max(0, Math.min(100, newPosition));
    this.updateClipPath();
  }

  // Handle slider change via input element (range slider)
  onSliderChange(event: Event): void {
    this.sliderPosition = +(event.target as HTMLInputElement).value;
    this.updateClipPath();
  }

  // Update the clip path of the after image for comparison effect
  private updateClipPath(): void {
    if (!this.afterImage || !this.slider) {
      return;
    }
    this.afterImage.nativeElement.style.clipPath = `inset(0 ${
      100 - this.sliderPosition
    }% 0 0)`;
  }

  // Handle like/dislike actions
  onLike(): void {
    this.isLiked = !this.isLiked;
    this.isDisliked = false;
  }

  onDislike(): void {
    this.isDisliked = !this.isDisliked;
    this.isLiked = false;
  }

  // Reset image URLs and return to upload page
  onDelete(): void {
    this.resetImages();
  }

  private resetImages(): void {
    this.beforeImageUrl = '';
    this.afterImageUrl = '';
    this.isUploadPage = true;
  }

  // Download the processed image
  downloadImage(): void {
    if (this.beforeImageUrl) {
      const link = document.createElement('a');
      link.href = this.beforeImageUrl;
      link.download = 'image.png';
      link.style.display = 'none';

      document.body.appendChild(link); // Append link to the body
      link.click(); // Programmatically click the link to trigger download
      document.body.removeChild(link); // Remove the link after download
    }
  }

  // Open GitHub profile link in a new tab
  openProfile(profile: any): void {
    window.open(profile.html_url, '_blank');
  }
}

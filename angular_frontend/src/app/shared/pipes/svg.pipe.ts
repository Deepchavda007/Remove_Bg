import { Pipe, PipeTransform, inject } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { icons } from '../../svg';

@Pipe({
  name: 'svg',
  standalone: true
})
export class SvgPipe implements PipeTransform {
  private icons = icons;
  private sanitizer = inject(DomSanitizer);

  transform(value: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(this.icons[value]);
  }
}

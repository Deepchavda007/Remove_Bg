import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AppService {
  private http = inject(HttpClient);

  getGithubProfile(username: string) {
    return this.http.get(`https://api.github.com/users/${username}`, {
      headers: {
        Authorization: `token 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`
      }
    });
  }

  uploadImage(formData: any) {
    return this.http.post(`${environment.apiUrl}/upload`, formData);
  }
}

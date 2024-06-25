import { Component } from '@angular/core';
import { Router } from '@angular/router';
@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent {
  public closedSidenavImage: string;
  public openedSidenavImage: string;
  constructor(protected router: Router) { }

  openAbout() {
    this.router.navigate(["/main/about"]);
  }
}

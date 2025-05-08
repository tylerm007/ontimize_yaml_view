import { ViewChild } from '@angular/core';
import { Component } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { OGridComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'Application-home',
  templateUrl: './Application-home.component.html',
  styleUrls: ['./Application-home.component.scss']
})
export class ApplicationHomeComponent {

  @ViewChild('grid') grid: OGridComponent;
  constructor(
    protected sanitizer: DomSanitizer,
  ) { }

  public openDetail( data: any): void {
    this.grid.viewDetail(data);
  }


  public getImageSrc(imgValue: string): any {
    return './assets/images/ontimize_web_log.png';
  }

}
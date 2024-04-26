import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { OTableButtonComponent, OTableComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'Entity-home',
  templateUrl: './Entity-home.component.html',
  styleUrls: ['./Entity-home.component.scss']
})
export class EntityHomeComponent implements AfterViewInit {

  @ViewChild('table', { static: true }) table: OTableComponent;

  @ViewChild('button')
  protected button: OTableButtonComponent;

  ngAfterViewInit() {
   // this.button.onClick.subscribe(event => {
   //   this.reportStoreService.openFillReport("94fa9d2a-e9cc-458a-a680-9bc576e14a38", {}, {});
   // });
  }

  //constructor(private reportStoreService: OReportStoreService) { }
}
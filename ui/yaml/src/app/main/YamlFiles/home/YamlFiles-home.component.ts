import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { OTableButtonComponent, OTableComponent } from 'ontimize-web-ngx';


@Component({
  selector: 'YamlFiles-home',
  templateUrl: './YamlFiles-home.component.html',
  styleUrls: ['./YamlFiles-home.component.scss']
})
export class YamlFilesHomeComponent implements AfterViewInit {

  @ViewChild('table', { static: true }) table: OTableComponent;

  @ViewChild('button')
  protected button: OTableButtonComponent;

  ngAfterViewInit() {
    
  }

}
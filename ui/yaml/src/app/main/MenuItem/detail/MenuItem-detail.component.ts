import { Injector, ViewChild, Component, OnInit, ViewEncapsulation } from '@angular/core';
import { OFormComponent, OntimizeService, OListPickerComponent, OTableComponent, ORealPipe, ONIFInputComponent } from 'ontimize-web-ngx';


@Component({
  selector: 'MenuItem-detail',
  templateUrl: './MenuItem-detail.component.html',
  styleUrls: ['./MenuItem-detail.component.scss']
})
export class MenuItemDetailComponent implements OnInit  {
  protected service: OntimizeService;
  protected data : any;
  @ViewChild('oDetailForm') form: OFormComponent;
  
  constructor(protected injector: Injector) {
    this.service = this.injector.get(OntimizeService);
  }

  ngOnInit() {
    this.configureService();
  }

  protected configureService() {
    const conf = this.service.getDefaultServiceConfiguration();
    conf['path'] = '/MenuItem';
    this.service.configureService(conf);
  }
  onDataLoaded(e: object) {
    console.log(JSON.stringify(e));
    this.data = e;
  }
  rebuildMenuItem() {
    
    console.log('MenuItem has been rebuilt.');
    // app_name = 'app' // TODO get from parent
    this.service.update({'id': this.data.id },{'rebuild': true,"app_name":"app","api_endpoint": this.data.entity_name}, 'MenuItem').subscribe((response) => {
      console.log('MenuItem rebuild response:', response);
      //snackbar
    }
    , (error) => {
      console.error('Error rebuilding MenuItem:', error);
      // Handle the error if needed
    }
    );  
  } 
}
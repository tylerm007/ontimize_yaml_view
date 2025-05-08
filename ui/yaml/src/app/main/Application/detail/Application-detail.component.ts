import { Injector, ViewChild, Component, OnInit, ViewEncapsulation } from '@angular/core';
import { OFormComponent, OntimizeService, OListPickerComponent, OTableComponent, ORealPipe, ONIFInputComponent } from 'ontimize-web-ngx';


@Component({
  selector: 'Application-detail',
  templateUrl: './Application-detail.component.html',
  styleUrls: ['./Application-detail.component.scss']
})
export class ApplicationDetailComponent implements OnInit  {
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
    conf['path'] = '/Application';
    this.service.configureService(conf);
  }
  onDataLoaded(e: object) {
    console.log(JSON.stringify(e));
    this.data = e;
  }
  rebuildApplication() {
    
    console.log('Application has been rebuilt.', JSON.stringify(this.data));
    this.service.update({'id': this.data.id },{'rebuild_flag': true,'file_path': this.data.file_path}, 'Application').subscribe((response) => {
      console.log('Application rebuild response:', response);
      //snackbar
    }
    , (error) => {
      console.error('Error rebuilding Application:', error);
      // Handle the error if needed
    }
    );  
  } 
  reloadApplication() {
    console.log('Application has been reloaded.', JSON.stringify(this.data));
    this.service.update({'id': this.data.id },{'reload_flag': true,'file_path': this.data.file_path}, 'Application').subscribe((response) => {
      console.log('Application reload response:', response);
      //snackbar
    }
    , (error) => {
      console.error('Error reloading Application:', error);
      // Handle the error if needed
    }
    );  
  }
}
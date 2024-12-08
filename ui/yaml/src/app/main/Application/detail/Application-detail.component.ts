import { Injector, ViewChild, Component, OnInit, ViewEncapsulation } from '@angular/core';
import { OFormComponent, OntimizeService, OListPickerComponent, OTableComponent, ORealPipe, ONIFInputComponent,DialogService, SnackBarService, OSnackBarConfig } from 'ontimize-web-ngx';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'Application-detail',
  templateUrl: './Application-detail.component.html',
  styleUrls: ['./Application-detail.component.scss']
})
export class ApplicationDetailComponent implements OnInit  {
  protected service: OntimizeService;
  protected entity: any;
  protected dialogService: any;
  protected dialog: any
  public snackBarService: SnackBarService;
  public snackBarConfig: OSnackBarConfig;

  @ViewChild('oDetailForm') form: OFormComponent;
  
  constructor(protected injector: Injector) {
    this.service = this.injector.get(OntimizeService);
    this.dialogService = this.injector.get(DialogService);
    this.dialog = this.injector.get(MatDialog);
    this.snackBarService = this.injector.get(SnackBarService);
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
    this.entity = e;
  }
  build(){
    console.log("build....")
    const configuration: OSnackBarConfig = {
      action: 'Ok',
      milliseconds: 2000,
      icon: 'check_circle',
      iconPosition: 'left'
    }
    this.snackBarService.open("Please wait, Building..", configuration);
      this.service.query({'app_name': this.entity.app_short_name},
        [],
        'build').subscribe((resp) => {
      console.log("build: " + JSON.stringify(resp.data));
      if (resp.code === 0) {
  
      } else {
        console.error(resp);
      }
    });
  }

}
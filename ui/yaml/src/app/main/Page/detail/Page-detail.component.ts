import { Injector, ViewChild, Component, OnInit, ViewEncapsulation } from '@angular/core';
import { OFormComponent, OntimizeService, OListPickerComponent, OTableComponent, ORealPipe, ONIFInputComponent } from 'ontimize-web-ngx';
import { ListReorderDialogComponent } from '../../ListReorderDialog/list-reorder-dialog.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'Page-detail',
  templateUrl: './Page-detail.component.html',
  styleUrls: ['./Page-detail.component.scss']
})
export class PageDetailComponent implements OnInit  {
  protected service: OntimizeService;
  public commaSeparatedList = 'apple, banana, orange, grape, melon';
  public visibilityStatus: Array<{value: string, visible: boolean}> = [];
  public data: any;
  
  @ViewChild('table', { static: true }) table: OTableComponent;

  
  @ViewChild('oDetailForm') form: OFormComponent;
  
  constructor(protected injector: Injector, public dialog: MatDialog) {
    this.service = this.injector.get(OntimizeService);
    this.dialog = this.injector.get(MatDialog);
  }

  ngOnInit() {
    this.configureService();
    
  }

  protected configureService() {
    const conf = this.service.getDefaultServiceConfiguration();
    conf['path'] = '/Page';
    this.service.configureService(conf);
  }
  onDataLoaded(e: object) {
    console.log(JSON.stringify(e));
    this.commaSeparatedList = e['visible_columns']
    this.data = e;
  }
  openReorderDialog(): void {
    console.log('openReorderDialog');
    const dialogRef = this.dialog.open(ListReorderDialogComponent, {
      width: '500px',
      data: { commaSeparatedList: this.commaSeparatedList }
    });
  
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.commaSeparatedList = result.commaSeparatedList;
        this.visibilityStatus = result.items;
        console.log('Dialog result:', result);
        console.log('Comma-separated list:', this.commaSeparatedList);
        console.log('Visibility status:', this.visibilityStatus);
        //this.updateVisibilityStatus();
        // you must have at least 1 column visible
        this.data.visible_columns = this.commaSeparatedList;
      
        this.updateProcessFlag();
      }
    });

    
  }
  updateProcessFlag() {
    console.log("updateProcessFlag");
    this.service.update({'id':this.data.id}, {'visible_columns':this.data.visible_columns},"Page").subscribe((resp: any) => {
   //this.service.update({'name':this.data.name}, {'upload_flag':true},"YamlFiles").subscribe((resp) => {
      console.log("res: " + JSON.stringify(resp));
      if (resp.code === 0) {
        console.log("updated: " + JSON.stringify(resp));
        this.form.setFieldValues({'visible_columns':this.data.visible_columns});
      } else {
        console.log("error: " + JSON.stringify(resp));
      }
    });
  }
}
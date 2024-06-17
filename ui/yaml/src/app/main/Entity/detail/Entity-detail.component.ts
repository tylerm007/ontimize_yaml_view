import { Injector, ViewChild, Component, OnInit, ViewEncapsulation } from '@angular/core';
import { OTableVisibleColumnsDialogComponent, OButtonComponent, OFormComponent, OntimizeService, OListPickerComponent, OTableComponent, DialogService} from 'ontimize-web-ngx';
import { environment } from 'src/environments/environment';
//import { OTableVisibleColumnsDialogComponent } from './visible-columns/o-table-visible-columns-dialog.component';  // This import is missing in the original file  
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'Entity-detail',
  templateUrl: './Entity-detail.component.html',
  styleUrls: ['./Entity-detail.component.scss']
})
export class EntityDetailComponent implements OnInit  {
  protected service: OntimizeService;
  protected entity: any;
  protected dialogService: DialogService;
  protected dialog: MatDialog
  //protected cd: ChangeDetectorRef,
  

  @ViewChild('table', { static: true }) table: OTableComponent;

  @ViewChild('button')
  protected button: OButtonComponent;

  @ViewChild('oDetailForm') form: OFormComponent;
  
  constructor(protected injector: Injector)  {
    this.service = this.injector.get(OntimizeService);
    this.dialogService = this.injector.get(DialogService);
  }
  ngOnInit() {
    this.configureService();
   
  }

  protected configureService() {
    const conf = this.service.getDefaultServiceConfiguration();
    conf['path'] = '/Entity';
    this.service.configureService(conf);
  }
  onDataLoaded(e: object) {
    console.log(JSON.stringify(e));
    this.entity = e;
  }
  
  showHideColumns() {
    // TODO - get the attributes for this table and pass them to the dialog
    // columns: ColumnVisibilityConfiguration[] = [];
    // Each column should have the following properties:
    //  attr: oCol.attr,
    //  title: oCol.label,
    //  visible: oCol.visible
    console.log("Show/Hide Columns:", this.entity);
    const dialogRef = this.dialog.open(OTableVisibleColumnsDialogComponent, {
      data: {
        table: this.entity
      },
      maxWidth: '35vw',
      disableClose: true,
      panelClass: ['o-dialog-class', 'o-table-dialog']
    });
    // POST the new column visibility to the server and refresh the table
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
    });
  }
}
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ApplicationHomeComponent } from './home/Application-home.component';
import { ApplicationNewComponent } from './new/Application-new.component';
import { ApplicationDetailComponent } from './detail/Application-detail.component';

const routes: Routes = [
  {path: '', component: ApplicationHomeComponent},
  { path: 'new', component: ApplicationNewComponent },
  { path: ':id', component: ApplicationDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Application-detail-permissions'
      }
    }
  },{
    path: ':application_id/MenuGroup', loadChildren: () => import('../MenuGroup/MenuGroup.module').then(m => m.MenuGroupModule),
    data: {
        oPermission: {
            permissionId: 'MenuGroup-detail-permissions'
        }
    }
}
];

export const APPLICATION_MODULE_DECLARATIONS = [
    ApplicationHomeComponent,
    ApplicationNewComponent,
    ApplicationDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ApplicationRoutingModule { }
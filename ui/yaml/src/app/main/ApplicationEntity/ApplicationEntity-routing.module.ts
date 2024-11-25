import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ApplicationEntityHomeComponent } from './home/ApplicationEntity-home.component';
import { ApplicationEntityNewComponent } from './new/ApplicationEntity-new.component';
import { ApplicationEntityDetailComponent } from './detail/ApplicationEntity-detail.component';

const routes: Routes = [
  {path: '', component: ApplicationEntityHomeComponent},
  { path: 'new', component: ApplicationEntityNewComponent },
  { path: ':application_name/:entity_name', component: ApplicationEntityDetailComponent,
    data: {
      oPermission: {
        permissionId: 'ApplicationEntity-detail-permissions'
      }
    }
  }
];

export const APPLICATIONENTITY_MODULE_DECLARATIONS = [
    ApplicationEntityHomeComponent,
    ApplicationEntityNewComponent,
    ApplicationEntityDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ApplicationEntityRoutingModule { }
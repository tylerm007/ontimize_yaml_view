import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RuleEventHomeComponent } from './home/RuleEvent-home.component';
import { RuleEventNewComponent } from './new/RuleEvent-new.component';
import { RuleEventDetailComponent } from './detail/RuleEvent-detail.component';

const routes: Routes = [
  {path: '', component: RuleEventHomeComponent},
  { path: 'new', component: RuleEventNewComponent },
  { path: ':id', component: RuleEventDetailComponent,
    data: {
      oPermission: {
        permissionId: 'RuleEvent-detail-permissions'
      }
    }
  }
];

export const RULEEVENT_MODULE_DECLARATIONS = [
    RuleEventHomeComponent,
    RuleEventNewComponent,
    RuleEventDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RuleEventRoutingModule { }
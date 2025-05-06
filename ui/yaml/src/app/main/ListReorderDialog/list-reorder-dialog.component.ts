import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';

export interface ListItem {
    value: string;
    visible: boolean;
}

export interface DialogData {
    commaSeparatedList: string;
}

@Component({
    selector: 'app-list-reorder-dialog',
    templateUrl: './list-reorder-dialog.component.html',
    styleUrls: ['./list-reorder-dialog.component.scss']
})
export class ListReorderDialogComponent implements OnInit {
    items: ListItem[] = [];

    constructor(
        public dialogRef: MatDialogRef<ListReorderDialogComponent>,
        @Inject(MAT_DIALOG_DATA) public data: DialogData
    ) { }

    ngOnInit(): void {
        // Convert comma-separated string to array of items
        if (this.data.commaSeparatedList) {
            this.items = this.data.commaSeparatedList
                .split(',')
                .map(item => item.trim())
                .filter(item => item !== '')
                .map(value => ({ value, visible: true }));
        }
    }

    drop(event: CdkDragDrop<ListItem[]>): void {
        moveItemInArray(this.items, event.previousIndex, event.currentIndex);
    }

    toggleVisibility(item: ListItem): void {
        item.visible = !item.visible;
    }

    onCancel(): void {
        this.dialogRef.close();
    }

    onSave(): void {
        // Convert items back to comma-separated string
        const result = {
            commaSeparatedList: this.items.map(item => item.value).join(', '),
            items: this.items // Return the full item objects with visibility info
        };
        this.dialogRef.close(result);
    }

    addItem(): void {
        this.items.push({ value: '', visible: true });
    }

    removeItem(index: number): void {
        this.items.splice(index, 1);
    }
}
// Component interfaces: Pass data and functions between components
import { Exam } from './data.interface';


export interface CreateModalProps {
    dialogOpen: boolean,
    setDialogOpen: (open: boolean) => void;
    onCreated: () => void;
}

export interface ItemComponentProps<T> {
    data: T;
    onDelete: () => void;
    isSelected: boolean;
}
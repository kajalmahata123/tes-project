// src/services/documentService.ts
import api from './api';
import { Document, DocumentUploadRequest, DocumentUploadResponse } from '../types/document';

export const documentService = {
  /**
   * Upload a document to the API
   * @param uploadRequest Document upload request with file and metadata
   * @returns Promise with upload response
   */
  uploadDocument: async (uploadRequest: DocumentUploadRequest): Promise<DocumentUploadResponse> => {
    const formData = new FormData();
    formData.append('file', uploadRequest.file);
    formData.append('document_type', uploadRequest.document_type);
    
    if (uploadRequest.document_description) {
      formData.append('document_description', uploadRequest.document_description);
    }
    
    if (uploadRequest.add_to_vector_db !== undefined) {
      formData.append('add_to_vector_db', String(uploadRequest.add_to_vector_db));
    }
    
    const response = await api.post<DocumentUploadResponse>('/document/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  /**
   * Get document metadata by ID
   * @param documentId Document ID
   * @returns Promise with document metadata
   */
  getDocument: async (documentId: string): Promise<Document> => {
    const response = await api.get<Document>(`/documents/${documentId}`);
    return response.data;
  },

  /**
   * Delete a document
   * @param documentId ID of the document to delete
   * @returns Promise resolving to void on success
   */
  deleteDocument: async (documentId: string): Promise<void> => {
    await api.delete(`/documents/${documentId}`);
  },
};

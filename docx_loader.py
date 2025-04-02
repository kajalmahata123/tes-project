// src/components/documents/DocumentUpload.tsx
import React, { useState, useRef } from 'react';
import { DocumentUploadRequest } from '../../types/document';
import Button from '../common/Button';
import Input from '../common/Input';
import { documentService } from '../../services/documentService';

// Define document types
type DocumentType = 'pdf' | 'openapi' | 'openai' | 'office' | 'text' | 'html';

// Update the DocumentUploadRequest type definition to extend the allowed document types
// Note: You'll need to update this in your types/document.ts file as well
interface ExtendedDocumentUploadRequest extends Omit<DocumentUploadRequest, 'document_type'> {
  document_type: DocumentType;
}

interface DocumentTypeConfig {
  label: string;
  accept: string;
  validExtensions: string[];
  mimeTypes?: string[];
}

interface DocumentUploadProps {
  onUploadSuccess: () => void;
  className?: string;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({
  onUploadSuccess,
  className = ''
}) => {
  const [file, setFile] = useState<File | null>(null);
  const [documentType, setDocumentType] = useState<DocumentType>('pdf');
  const [description, setDescription] = useState('');
  const [addToVectorDb, setAddToVectorDb] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Map document types to their accepted file extensions
  const documentTypeConfigs: Record<DocumentType, DocumentTypeConfig> = {
    pdf: {
      label: 'PDF Document',
      accept: '.pdf',
      validExtensions: ['pdf'],
      mimeTypes: ['application/pdf']
    },
    openapi: {
      label: 'OpenAPI Specification',
      accept: '.json,.yaml,.yml',
      validExtensions: ['json', 'yaml', 'yml']
    },
    openai: {
      label: 'OpenAI JSON',
      accept: '.json',
      validExtensions: ['json']
    },
    office: {
      label: 'Office Documents',
      accept: '.doc,.docx',
      validExtensions: ['doc', 'docx']
    },
    text: {
      label: 'Text Documents',
      accept: '.txt,.md,.csv',
      validExtensions: ['txt', 'md', 'csv']
    },
    html: {
      label: 'HTML Documents',
      accept: '.html,.htm',
      validExtensions: ['html', 'htm']
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);

    // Reset error when file changes
    if (selectedFile) {
      setError(null);
    }
  };

  const validateFile = (): boolean => {
    if (!file) {
      setError('Please select a file');
      return false;
    }

    const fileExt = file.name.split('.').pop()?.toLowerCase() || '';
    const config = documentTypeConfigs[documentType];

    // For PDF, check MIME type if available
    if (documentType === 'pdf' && config.mimeTypes && !config.mimeTypes.includes(file.type)) {
      setError('File must be a valid PDF document');
      return false;
    }

    // For all document types, check file extension
    if (!config.validExtensions.includes(fileExt)) {
      setError(`File must be a valid ${config.label} (${config.validExtensions.join(', ')})`);
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateFile()) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Cast to the extended request type
      const uploadRequest: ExtendedDocumentUploadRequest = {
        file: file as File,
        document_type: documentType,
        document_description: description || undefined,
        add_to_vector_db: addToVectorDb
      };

      // Cast back to the original type when calling the service
      // Note: In production, you should update the service to handle the new types
      await documentService.uploadDocument(uploadRequest as unknown as DocumentUploadRequest);

      // Reset form
      setFile(null);
      setDescription('');
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }

      // Notify parent of successful upload
      onUploadSuccess();

    } catch (err: any) {
      console.error('Upload error:', err);
      setError(err.response?.data?.detail || 'Failed to upload document');
    } finally {
      setIsLoading(false);
    }
  };

  const getAcceptedFileTypes = () => {
    return documentTypeConfigs[documentType].accept;
  };

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      <h2 className="text-xl font-semibold mb-4">Upload Document</h2>

      <form onSubmit={handleSubmit}>
        {/* Document Type */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-secondary-700 mb-1">
            Document Type
          </label>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
            {Object.entries(documentTypeConfigs).map(([type, config]) => (
              <label key={type} className="inline-flex items-center p-2 border rounded hover:bg-gray-50">
                <input
                  type="radio"
                  className="form-radio text-primary-600"
                  checked={documentType === type}
                  onChange={() => setDocumentType(type as DocumentType)}
                />
                <span className="ml-2 text-sm">{config.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* File Input */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-secondary-700 mb-1">
            Select File
          </label>
          <div className="mt-1 flex items-center">
            <input
              ref={fileInputRef}
              type="file"
              accept={getAcceptedFileTypes()}
              onChange={handleFileChange}
              className="block w-full text-sm text-secondary-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-md file:border-0
                file:text-sm file:font-medium
                file:bg-primary-50 file:text-primary-700
                hover:file:bg-primary-100
                focus:outline-none"
            />
          </div>
          {file && (
            <p className="mt-1 text-sm text-secondary-500">
              Selected: {file.name} ({Math.round(file.size / 1024)} KB)
            </p>
          )}
        </div>

        {/* Description */}
        <div className="mb-4">
          <Input
            label="Description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Enter a description for this document"
            fullWidth
          />
        </div>

        {/* Vector DB Option */}
        <div className="mb-6">
          <label className="inline-flex items-center">
            <input
              type="checkbox"
              className="form-checkbox rounded text-primary-600"
              checked={addToVectorDb}
              onChange={(e) => setAddToVectorDb(e.target.checked)}
            />
            <span className="ml-2">Add to vector database for searching</span>
          </label>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-4 p-3 bg-error-50 text-error-700 rounded-md border border-error-200">
            {error}
          </div>
        )}

        {/* Submit Button */}
        <Button
          type="submit"
          isLoading={isLoading}
          disabled={isLoading || !file}
          fullWidth
        >
          Upload Document
        </Button>
      </form>
    </div>
  );
};

export default DocumentUpload;

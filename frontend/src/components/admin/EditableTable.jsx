// src/components/EditableTable.js
import React, { useState, useEffect } from "react";
import { AgGridReact } from "ag-grid-react";  // Import the ag-Grid React component
import { updateRecord, deleteRecord, addRecord } from "./api";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";


const EditableTable = ({ data, entity }) => {
  const [rowData, setRowData] = useState(data);
  const [columnDefs, setColumnDefs] = useState([]);

  // Set column definitions dynamically based on entity
  useEffect(() => {
    if (data.length > 0) {
      const columns = Object.keys(data[0]).map((key) => ({
        headerName: key.charAt(0).toUpperCase() + key.slice(1),
        field: key,
        editable: true, // Make all cells editable
        resizable: true,
      }));
      setColumnDefs(columns);
    }
  }, [data]);

  const handleSave = async () => {
    for (const record of rowData) {
      await updateRecord(entity, record.id, record); // send all record attributes
    }
  };

  const handleDelete = async (id) => {
    await deleteRecord(entity, id);
    setRowData(rowData.filter((item) => item.id !== id));
  };

  const handleAdd = async () => {
    const newRecord = {}; // Create a new empty record (you can pre-populate it if needed)
    const addedRecord = await addRecord(entity, newRecord);
    setRowData([...rowData, addedRecord]);
  };

  const gridOptions = {
    domLayout: 'autoHeight', // Automatically adjust the height of the grid based on rows
    pagination: true,        // Enable pagination
    paginationPageSize: 20,  // Set the number of rows per page
    defaultColDef: {
      resizable: true,
    },
  };

  const onFirstDataRendered = (params) => {
    params.api.sizeColumnsToFit();
  };

  function generateButtonText (entity){
    if(['users', 'trips', 'ports', 'restaurants', 'ships', 'packages'].indexOf(entity) !== -1) {
        return entity.slice(0, entity.length-1);
    } else {
        return entity.slice(0, entity.length - 3) + 'y';
    }
  }

  return (
    <div>
      {/* {entity !== 'users' && <button onClick={handleAdd}>Add {generateButtonText(entity)}</button>}  */}
      <div className="ag-theme-alpine" style={{ width: "100%", height: "500px" }}>
        <AgGridReact
          gridOptions={gridOptions}
          columnDefs={columnDefs}
          rowData={rowData}
          onGridReady={(params) => params.api.sizeColumnsToFit()} // Resize columns to fit the grid
          onFirstDataRendered={onFirstDataRendered}
        />
      </div>
      <button onClick={handleSave}>Save Changes</button>
    </div>
  );
};

export default EditableTable;

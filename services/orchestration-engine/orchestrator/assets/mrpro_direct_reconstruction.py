import mrpro
from dagster import AssetIn, AssetKey, asset
from scanhub_libraries.resources import IDATA_IO_KEY
from scanhub_libraries.resources.dag_config import DAGConfiguration

from orchestrator.hooks import notify_dag_success
from orchestrator.io.acquisition_data import AcquisitionData, acquisition_data_asset
from orchestrator.io.idata_io_manager import IDataContext


@asset(
    group_name="reconstruction",
    description="MRpro direct reconstruction.",
    ins={"data": AssetIn(key=acquisition_data_asset.key)},
    io_manager_key=IDATA_IO_KEY,
    hooks={notify_dag_success},
)
def mrpro_direct_reconstruction(context, data: AcquisitionData, dag_config: DAGConfiguration) -> IDataContext:
    """Reconstruct image from a list acquisition results.

    1. Loads acquisition results using the DataLakeRessource providing mrd path and meta data.
    2. Loads mrpro KData object from mrd path
    3. Performs image reconstruction using the direct reconstruction method from mrpro.
    4. Return the reconstructed IData object -> Return is passed to the idata_io_manager.
    """
    mrd_input = data.mrd_path
    context.log.info("Reading MRD input: %s", str(mrd_input))
    trajectory_calculator = mrpro.data.traj_calculators.KTrajectoryCartesian()
    kdata = mrpro.data.KData.from_file(mrd_input, trajectory_calculator)
    context.log.info("Loaded data: %s", kdata.shape)
    reconstruction = mrpro.algorithms.reconstruction.DirectReconstruction(kdata)
    context.log.info("Performing direct reconstruction using mrpro...")
    idata = reconstruction(kdata)
    return IDataContext(data=idata, dag_config=dag_config)

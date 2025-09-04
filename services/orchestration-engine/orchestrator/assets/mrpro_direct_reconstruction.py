import mrpro
from dagster import AssetIn, AssetKey, asset
from scanhub_libraries.resources import DAGConfiguration

from orchestrator.assets.acquisition import AcquisitionData
from orchestrator.hooks.scanhub import notify_dag_success
from orchestrator.io_managers.idata_io_manager import IDataContext


@asset(
    group_name="reconstruction",
    description="MRpro direct reconstruction.",
    ins={"data": AssetIn(key=AssetKey("read_acquisition_data"))},
    io_manager_key="idata_io_manager",
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

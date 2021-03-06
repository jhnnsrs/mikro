from mikro.traits import (
    Table,
    Representation,
    Sample,
    ROI,
    Vectorizable,
    Experiment,
    Thumbnail,
    OmeroFile,
)
from typing import Optional, List, Literal, AsyncIterator, Iterator, Dict
from mikro.funcs import execute, subscribe, asubscribe, aexecute
from pydantic import BaseModel, Field
from mikro.scalars import Store, XArray, Upload, File, DataFrame
from enum import Enum
from mikro.rath import MikroRath
from rath.scalars import ID


class OmeroFileType(str, Enum):
    """An enumeration."""

    TIFF = "TIFF"
    "Tiff"
    JPEG = "JPEG"
    "Jpeg"
    MSR = "MSR"
    "MSR File"
    CZI = "CZI"
    "Zeiss Microscopy File"
    UNKNOWN = "UNKNOWN"
    "Unwknon File Format"


class RepresentationVariety(str, Enum):
    """An enumeration."""

    MASK = "MASK"
    "Mask (Value represent Labels)"
    VOXEL = "VOXEL"
    "Voxel (Value represent Intensity)"
    RGB = "RGB"
    "RGB (First three channel represent RGB)"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class RepresentationVarietyInput(str, Enum):
    """Variety expresses the Type of Representation we are dealing with"""

    MASK = "MASK"
    "Mask (Value represent Labels)"
    VOXEL = "VOXEL"
    "Voxel (Value represent Intensity)"
    RGB = "RGB"
    "RGB (First three channel represent RGB)"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class ROIType(str, Enum):
    """An enumeration."""

    ELLIPSE = "ELLIPSE"
    "Ellipse"
    POLYGON = "POLYGON"
    "POLYGON"
    LINE = "LINE"
    "Line"
    RECTANGLE = "RECTANGLE"
    "Rectangle"
    PATH = "PATH"
    "Path"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class RoiTypeInput(str, Enum):
    """An enumeration."""

    ELLIPSIS = "ELLIPSIS"
    "Ellipse"
    POLYGON = "POLYGON"
    "POLYGON"
    LINE = "LINE"
    "Line"
    RECTANGLE = "RECTANGLE"
    "Rectangle"
    PATH = "PATH"
    "Path"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class OmeroRepresentationInput(BaseModel):
    planes: Optional[List[Optional["PlaneInput"]]]
    channels: Optional[List[Optional["ChannelInput"]]]
    physical_size: Optional["PhysicalSizeInput"] = Field(alias="physicalSize")
    scale: Optional[List[Optional[float]]]


class PlaneInput(BaseModel):
    z_index: Optional[int] = Field(alias="zIndex")
    y_index: Optional[int] = Field(alias="yIndex")
    x_index: Optional[int] = Field(alias="xIndex")
    c_index: Optional[int] = Field(alias="cIndex")
    t_index: Optional[int] = Field(alias="tIndex")
    exposure_time: Optional[float] = Field(alias="exposureTime")
    delta_t: Optional[float] = Field(alias="deltaT")


class ChannelInput(BaseModel):
    name: Optional[str]
    emmission_wavelength: Optional[float] = Field(alias="emmissionWavelength")
    excitation_wavelength: Optional[float] = Field(alias="excitationWavelength")
    acquisition_mode: Optional[str] = Field(alias="acquisitionMode")
    color: Optional[str]


class PhysicalSizeInput(BaseModel):
    x: Optional[int]
    y: Optional[int]
    z: Optional[int]
    t: Optional[int]
    c: Optional[int]


class InputVector(BaseModel, Vectorizable):
    x: Optional[float]
    "X-coordinate"
    y: Optional[float]
    "Y-coordinate"
    z: Optional[float]
    "Z-coordinate"


OmeroRepresentationInput.update_forward_refs()


class RepresentationFragmentSample(Sample, BaseModel):
    """Samples are storage containers for representations. A Sample is to be understood analogous to a Biological Sample. It existed in Time (the time of acquisiton and experimental procedure),
    was measured in space (x,y,z) and in different modalities (c). Sample therefore provide a datacontainer where each Representation of
    the data shares the same dimensions. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    """

    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    id: ID
    name: str

    class Config:
        frozen = True


class RepresentationFragment(Representation, BaseModel):
    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    sample: Optional[RepresentationFragmentSample]
    "The Sample this representation belongs to"
    type: Optional[str]
    "The Representation can have varying types, consult your API"
    id: ID
    store: Optional[Store]
    variety: RepresentationVariety
    "The Representation can have varying types, consult your API"
    name: Optional[str]
    "Cleartext name"

    class Config:
        frozen = True


class ThumbnailFragment(Thumbnail, BaseModel):
    typename: Optional[Literal["Thumbnail"]] = Field(alias="__typename")
    id: ID
    image: Optional[str]

    class Config:
        frozen = True


class ROIFragmentVectors(BaseModel):
    typename: Optional[Literal["Vector"]] = Field(alias="__typename")
    x: Optional[float]
    "X-coordinate"
    y: Optional[float]
    "Y-coordinate"
    z: Optional[float]
    "Z-coordinate"

    class Config:
        frozen = True


class ROIFragmentRepresentation(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID

    class Config:
        frozen = True


class ROIFragmentCreator(BaseModel):
    """A reflection on the real User"""

    typename: Optional[Literal["User"]] = Field(alias="__typename")
    email: str
    color: Optional[str]
    "The associated color for this user"

    class Config:
        frozen = True


class ROIFragment(ROI, BaseModel):
    typename: Optional[Literal["ROI"]] = Field(alias="__typename")
    id: ID
    vectors: Optional[List[Optional[ROIFragmentVectors]]]
    type: ROIType
    "The Representation can have varying types, consult your API"
    representation: Optional[ROIFragmentRepresentation]
    creator: ROIFragmentCreator

    class Config:
        frozen = True


class TableFragmentCreator(BaseModel):
    """A reflection on the real User"""

    typename: Optional[Literal["User"]] = Field(alias="__typename")
    email: str

    class Config:
        frozen = True


class TableFragmentSample(Sample, BaseModel):
    """Samples are storage containers for representations. A Sample is to be understood analogous to a Biological Sample. It existed in Time (the time of acquisiton and experimental procedure),
    was measured in space (x,y,z) and in different modalities (c). Sample therefore provide a datacontainer where each Representation of
    the data shares the same dimensions. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    """

    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    id: ID

    class Config:
        frozen = True


class TableFragmentRepresentation(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID

    class Config:
        frozen = True


class TableFragmentExperiment(Experiment, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants @elements/experiment"""

    typename: Optional[Literal["Experiment"]] = Field(alias="__typename")
    id: ID

    class Config:
        frozen = True


class TableFragment(Table, BaseModel):
    typename: Optional[Literal["Table"]] = Field(alias="__typename")
    id: ID
    name: str
    tags: Optional[List[Optional[str]]]
    "A comma-separated list of tags."
    store: Optional[str]
    "The location of the Parquet on the Storage System (S3 or Media-URL)"
    creator: Optional[TableFragmentCreator]
    sample: Optional[TableFragmentSample]
    representation: Optional[TableFragmentRepresentation]
    experiment: Optional[TableFragmentExperiment]

    class Config:
        frozen = True


class SampleFragmentRepresentations(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID

    class Config:
        frozen = True


class SampleFragmentExperiments(Experiment, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants @elements/experiment"""

    typename: Optional[Literal["Experiment"]] = Field(alias="__typename")
    id: ID

    class Config:
        frozen = True


class SampleFragment(Sample, BaseModel):
    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    name: str
    id: ID
    representations: Optional[List[Optional[SampleFragmentRepresentations]]]
    meta: Optional[Dict]
    experiments: List[SampleFragmentExperiments]

    class Config:
        frozen = True


class OmeroFileFragment(OmeroFile, BaseModel):
    typename: Optional[Literal["OmeroFile"]] = Field(alias="__typename")
    id: ID
    name: str
    file: Optional[File]

    class Config:
        frozen = True


class ExperimentFragmentCreator(BaseModel):
    """A reflection on the real User"""

    typename: Optional[Literal["User"]] = Field(alias="__typename")
    email: str

    class Config:
        frozen = True


class ExperimentFragment(Experiment, BaseModel):
    typename: Optional[Literal["Experiment"]] = Field(alias="__typename")
    id: ID
    name: str
    creator: Optional[ExperimentFragmentCreator]
    meta: Optional[Dict]

    class Config:
        frozen = True


class Get_omero_fileQuery(BaseModel):
    omerofile: Optional[OmeroFileFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment OmeroFile on OmeroFile {\n  id\n  name\n  file\n}\n\nquery get_omero_file($id: ID!) {\n  omerofile(id: $id) {\n    ...OmeroFile\n  }\n}"

    class Config:
        frozen = True


class Expand_omerofileQuery(BaseModel):
    omerofile: Optional[OmeroFileFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment OmeroFile on OmeroFile {\n  id\n  name\n  file\n}\n\nquery expand_omerofile($id: ID!) {\n  omerofile(id: $id) {\n    ...OmeroFile\n  }\n}"

    class Config:
        frozen = True


class Search_omerofileQueryOmerofiles(OmeroFile, BaseModel):
    typename: Optional[Literal["OmeroFile"]] = Field(alias="__typename")
    id: ID
    label: str

    class Config:
        frozen = True


class Search_omerofileQuery(BaseModel):
    omerofiles: Optional[List[Optional[Search_omerofileQueryOmerofiles]]]
    "My samples return all of the users samples attached to the current user"

    class Arguments(BaseModel):
        search: str

    class Meta:
        document = "query search_omerofile($search: String!) {\n  omerofiles(name: $search) {\n    id: id\n    label: name\n  }\n}"

    class Config:
        frozen = True


class Expand_representationQuery(BaseModel):
    representation: Optional[RepresentationFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Representation on Representation {\n  sample {\n    id\n    name\n  }\n  type\n  id\n  store\n  variety\n  name\n}\n\nquery expand_representation($id: ID!) {\n  representation(id: $id) {\n    ...Representation\n  }\n}"

    class Config:
        frozen = True


class Get_representationQuery(BaseModel):
    representation: Optional[RepresentationFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Representation on Representation {\n  sample {\n    id\n    name\n  }\n  type\n  id\n  store\n  variety\n  name\n}\n\nquery get_representation($id: ID!) {\n  representation(id: $id) {\n    ...Representation\n  }\n}"

    class Config:
        frozen = True


class Search_representationQueryRepresentations(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    value: ID
    label: Optional[str]
    "Cleartext name"

    class Config:
        frozen = True


class Search_representationQuery(BaseModel):
    representations: Optional[List[Optional[Search_representationQueryRepresentations]]]
    "All represetations"

    class Arguments(BaseModel):
        search: Optional[str] = None

    class Meta:
        document = "query search_representation($search: String) {\n  representations(name: $search, limit: 20) {\n    value: id\n    label: name\n  }\n}"

    class Config:
        frozen = True


class Get_random_repQuery(BaseModel):
    random_representation: Optional[RepresentationFragment] = Field(
        alias="randomRepresentation"
    )
    "Get a single representation by ID"

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment Representation on Representation {\n  sample {\n    id\n    name\n  }\n  type\n  id\n  store\n  variety\n  name\n}\n\nquery get_random_rep {\n  randomRepresentation {\n    ...Representation\n  }\n}"

    class Config:
        frozen = True


class ThumbnailQuery(BaseModel):
    thumbnail: Optional[ThumbnailFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Thumbnail on Thumbnail {\n  id\n  image\n}\n\nquery Thumbnail($id: ID!) {\n  thumbnail(id: $id) {\n    ...Thumbnail\n  }\n}"

    class Config:
        frozen = True


class Expand_thumbnailQuery(BaseModel):
    thumbnail: Optional[ThumbnailFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Thumbnail on Thumbnail {\n  id\n  image\n}\n\nquery expand_thumbnail($id: ID!) {\n  thumbnail(id: $id) {\n    ...Thumbnail\n  }\n}"

    class Config:
        frozen = True


class Get_roisQuery(BaseModel):
    rois: Optional[List[Optional[ROIFragment]]]
    "All represetations"

    class Arguments(BaseModel):
        representation: ID
        type: Optional[List[Optional[RoiTypeInput]]] = None

    class Meta:
        document = "fragment ROI on ROI {\n  id\n  vectors {\n    x\n    y\n    z\n  }\n  type\n  representation {\n    id\n  }\n  creator {\n    email\n    color\n  }\n}\n\nquery get_rois($representation: ID!, $type: [RoiTypeInput]) {\n  rois(representation: $representation, type: $type) {\n    ...ROI\n  }\n}"

    class Config:
        frozen = True


class TableQuery(BaseModel):
    table: Optional[TableFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Table on Table {\n  id\n  name\n  tags\n  store\n  creator {\n    email\n  }\n  sample {\n    id\n  }\n  representation {\n    id\n  }\n  experiment {\n    id\n  }\n}\n\nquery Table($id: ID!) {\n  table(id: $id) {\n    ...Table\n  }\n}"

    class Config:
        frozen = True


class Expand_tableQuery(BaseModel):
    table: Optional[TableFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Table on Table {\n  id\n  name\n  tags\n  store\n  creator {\n    email\n  }\n  sample {\n    id\n  }\n  representation {\n    id\n  }\n  experiment {\n    id\n  }\n}\n\nquery expand_table($id: ID!) {\n  table(id: $id) {\n    ...Table\n  }\n}"

    class Config:
        frozen = True


class Search_tablesQueryTables(Table, BaseModel):
    typename: Optional[Literal["Table"]] = Field(alias="__typename")
    id: ID
    label: str

    class Config:
        frozen = True


class Search_tablesQuery(BaseModel):
    tables: Optional[List[Optional[Search_tablesQueryTables]]]
    "My samples return all of the users samples attached to the current user"

    class Arguments(BaseModel):
        pass

    class Meta:
        document = (
            "query search_tables {\n  tables {\n    id: id\n    label: name\n  }\n}"
        )

    class Config:
        frozen = True


class Get_sampleQuery(BaseModel):
    sample: Optional[SampleFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Sample on Sample {\n  name\n  id\n  representations {\n    id\n  }\n  meta\n  experiments {\n    id\n  }\n}\n\nquery get_sample($id: ID!) {\n  sample(id: $id) {\n    ...Sample\n  }\n}"

    class Config:
        frozen = True


class Search_sampleQuerySamples(Sample, BaseModel):
    """Samples are storage containers for representations. A Sample is to be understood analogous to a Biological Sample. It existed in Time (the time of acquisiton and experimental procedure),
    was measured in space (x,y,z) and in different modalities (c). Sample therefore provide a datacontainer where each Representation of
    the data shares the same dimensions. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    """

    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    value: ID
    label: str

    class Config:
        frozen = True


class Search_sampleQuery(BaseModel):
    samples: Optional[List[Optional[Search_sampleQuerySamples]]]
    "All Samples"

    class Arguments(BaseModel):
        search: Optional[str] = None

    class Meta:
        document = "query search_sample($search: String) {\n  samples(name: $search, limit: 20) {\n    value: id\n    label: name\n  }\n}"

    class Config:
        frozen = True


class Expand_sampleQuery(BaseModel):
    sample: Optional[SampleFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Sample on Sample {\n  name\n  id\n  representations {\n    id\n  }\n  meta\n  experiments {\n    id\n  }\n}\n\nquery expand_sample($id: ID!) {\n  sample(id: $id) {\n    ...Sample\n  }\n}"

    class Config:
        frozen = True


class Get_experimentQuery(BaseModel):
    experiment: Optional[ExperimentFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Experiment on Experiment {\n  id\n  name\n  creator {\n    email\n  }\n  meta\n}\n\nquery get_experiment($id: ID!) {\n  experiment(id: $id) {\n    ...Experiment\n  }\n}"

    class Config:
        frozen = True


class Expand_experimentQuery(BaseModel):
    experiment: Optional[ExperimentFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Experiment on Experiment {\n  id\n  name\n  creator {\n    email\n  }\n  meta\n}\n\nquery expand_experiment($id: ID!) {\n  experiment(id: $id) {\n    ...Experiment\n  }\n}"

    class Config:
        frozen = True


class Search_experimentQueryExperiments(Experiment, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants @elements/experiment"""

    typename: Optional[Literal["Experiment"]] = Field(alias="__typename")
    id: ID
    label: str

    class Config:
        frozen = True


class Search_experimentQuery(BaseModel):
    experiments: Optional[List[Optional[Search_experimentQueryExperiments]]]
    "All Samples"

    class Arguments(BaseModel):
        search: Optional[str] = None

    class Meta:
        document = "query search_experiment($search: String) {\n  experiments(name: $search, limit: 30) {\n    id: id\n    label: name\n  }\n}"

    class Config:
        frozen = True


class Watch_roisSubscriptionRois(BaseModel):
    typename: Optional[Literal["RoiEvent"]] = Field(alias="__typename")
    update: Optional[ROIFragment]
    delete: Optional[ID]
    create: Optional[ROIFragment]

    class Config:
        frozen = True


class Watch_roisSubscription(BaseModel):
    rois: Optional[Watch_roisSubscriptionRois]

    class Arguments(BaseModel):
        representation: ID

    class Meta:
        document = "fragment ROI on ROI {\n  id\n  vectors {\n    x\n    y\n    z\n  }\n  type\n  representation {\n    id\n  }\n  creator {\n    email\n    color\n  }\n}\n\nsubscription watch_rois($representation: ID!) {\n  rois(representation: $representation) {\n    update {\n      ...ROI\n    }\n    delete\n    create {\n      ...ROI\n    }\n  }\n}"

    class Config:
        frozen = True


class Watch_samplesSubscriptionMysamplesUpdateExperiments(Experiment, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants @elements/experiment"""

    typename: Optional[Literal["Experiment"]] = Field(alias="__typename")
    name: str

    class Config:
        frozen = True


class Watch_samplesSubscriptionMysamplesUpdate(Sample, BaseModel):
    """Samples are storage containers for representations. A Sample is to be understood analogous to a Biological Sample. It existed in Time (the time of acquisiton and experimental procedure),
    was measured in space (x,y,z) and in different modalities (c). Sample therefore provide a datacontainer where each Representation of
    the data shares the same dimensions. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    """

    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    id: ID
    name: str
    experiments: List[Watch_samplesSubscriptionMysamplesUpdateExperiments]

    class Config:
        frozen = True


class Watch_samplesSubscriptionMysamplesCreateExperiments(Experiment, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants @elements/experiment"""

    typename: Optional[Literal["Experiment"]] = Field(alias="__typename")
    name: str

    class Config:
        frozen = True


class Watch_samplesSubscriptionMysamplesCreate(Sample, BaseModel):
    """Samples are storage containers for representations. A Sample is to be understood analogous to a Biological Sample. It existed in Time (the time of acquisiton and experimental procedure),
    was measured in space (x,y,z) and in different modalities (c). Sample therefore provide a datacontainer where each Representation of
    the data shares the same dimensions. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    """

    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    name: str
    experiments: List[Watch_samplesSubscriptionMysamplesCreateExperiments]

    class Config:
        frozen = True


class Watch_samplesSubscriptionMysamples(BaseModel):
    typename: Optional[Literal["SamplesEvent"]] = Field(alias="__typename")
    update: Optional[Watch_samplesSubscriptionMysamplesUpdate]
    create: Optional[Watch_samplesSubscriptionMysamplesCreate]

    class Config:
        frozen = True


class Watch_samplesSubscription(BaseModel):
    my_samples: Optional[Watch_samplesSubscriptionMysamples] = Field(alias="mySamples")

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "subscription watch_samples {\n  mySamples {\n    update {\n      id\n      name\n      experiments {\n        name\n      }\n    }\n    create {\n      name\n      experiments {\n        name\n      }\n    }\n  }\n}"

    class Config:
        frozen = True


class NegotiateMutation(BaseModel):
    negotiate: Optional[Dict]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "mutation negotiate {\n  negotiate\n}"

    class Config:
        frozen = True


class Upload_bioimageMutationUploadomerofile(OmeroFile, BaseModel):
    typename: Optional[Literal["OmeroFile"]] = Field(alias="__typename")
    id: ID
    file: Optional[File]
    type: OmeroFileType
    name: str

    class Config:
        frozen = True


class Upload_bioimageMutation(BaseModel):
    upload_omero_file: Optional[Upload_bioimageMutationUploadomerofile] = Field(
        alias="uploadOmeroFile"
    )

    class Arguments(BaseModel):
        file: Upload

    class Meta:
        document = "mutation upload_bioimage($file: Upload!) {\n  uploadOmeroFile(file: $file) {\n    id\n    file\n    type\n    name\n  }\n}"

    class Config:
        frozen = True


class Create_size_featureMutationCreatesizefeatureLabelRepresentation(
    Representation, BaseModel
):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID

    class Config:
        frozen = True


class Create_size_featureMutationCreatesizefeatureLabel(BaseModel):
    typename: Optional[Literal["Label"]] = Field(alias="__typename")
    id: ID
    representation: Optional[
        Create_size_featureMutationCreatesizefeatureLabelRepresentation
    ]

    class Config:
        frozen = True


class Create_size_featureMutationCreatesizefeature(BaseModel):
    typename: Optional[Literal["SizeFeature"]] = Field(alias="__typename")
    id: ID
    size: float
    label: Optional[Create_size_featureMutationCreatesizefeatureLabel]

    class Config:
        frozen = True


class Create_size_featureMutation(BaseModel):
    create_size_feature: Optional[Create_size_featureMutationCreatesizefeature] = Field(
        alias="createSizeFeature"
    )
    "Creates a Sample"

    class Arguments(BaseModel):
        label: ID
        size: float
        creator: Optional[ID] = None

    class Meta:
        document = "mutation create_size_feature($label: ID!, $size: Float!, $creator: ID) {\n  createSizeFeature(label: $label, size: $size, creator: $creator) {\n    id\n    size\n    label {\n      id\n      representation {\n        id\n      }\n    }\n  }\n}"

    class Config:
        frozen = True


class Create_labelMutationCreatelabel(BaseModel):
    typename: Optional[Literal["Label"]] = Field(alias="__typename")
    id: ID
    instance: int

    class Config:
        frozen = True


class Create_labelMutation(BaseModel):
    create_label: Optional[Create_labelMutationCreatelabel] = Field(alias="createLabel")
    "Creates a Sample"

    class Arguments(BaseModel):
        instance: int
        representation: ID
        creator: ID
        name: Optional[str] = None

    class Meta:
        document = "mutation create_label($instance: Int!, $representation: ID!, $creator: ID!, $name: String) {\n  createLabel(\n    instance: $instance\n    representation: $representation\n    creator: $creator\n    name: $name\n  ) {\n    id\n    instance\n  }\n}"

    class Config:
        frozen = True


class From_xarrayMutation(BaseModel):
    from_x_array: Optional[RepresentationFragment] = Field(alias="fromXArray")
    "Creates a Representation"

    class Arguments(BaseModel):
        xarray: XArray
        name: Optional[str] = None
        variety: Optional[RepresentationVarietyInput] = None
        origins: Optional[List[Optional[ID]]] = None
        tags: Optional[List[Optional[str]]] = None
        sample: Optional[ID] = None
        omero: Optional[OmeroRepresentationInput] = None

    class Meta:
        document = "fragment Representation on Representation {\n  sample {\n    id\n    name\n  }\n  type\n  id\n  store\n  variety\n  name\n}\n\nmutation from_xarray($xarray: XArray!, $name: String, $variety: RepresentationVarietyInput, $origins: [ID], $tags: [String], $sample: ID, $omero: OmeroRepresentationInput) {\n  fromXArray(\n    xarray: $xarray\n    name: $name\n    origins: $origins\n    tags: $tags\n    sample: $sample\n    omero: $omero\n    variety: $variety\n  ) {\n    ...Representation\n  }\n}"

    class Config:
        frozen = True


class Double_uploadMutationX(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID
    store: Optional[Store]

    class Config:
        frozen = True


class Double_uploadMutationY(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID
    store: Optional[Store]

    class Config:
        frozen = True


class Double_uploadMutation(BaseModel):
    x: Optional[Double_uploadMutationX]
    "Creates a Representation"
    y: Optional[Double_uploadMutationY]
    "Creates a Representation"

    class Arguments(BaseModel):
        xarray: XArray
        name: Optional[str] = None
        origins: Optional[List[Optional[ID]]] = None
        tags: Optional[List[Optional[str]]] = None
        sample: Optional[ID] = None
        omero: Optional[OmeroRepresentationInput] = None

    class Meta:
        document = "mutation double_upload($xarray: XArray!, $name: String, $origins: [ID], $tags: [String], $sample: ID, $omero: OmeroRepresentationInput) {\n  x: fromXArray(\n    xarray: $xarray\n    name: $name\n    origins: $origins\n    tags: $tags\n    sample: $sample\n    omero: $omero\n  ) {\n    id\n    store\n  }\n  y: fromXArray(\n    xarray: $xarray\n    name: $name\n    origins: $origins\n    tags: $tags\n    sample: $sample\n    omero: $omero\n  ) {\n    id\n    store\n  }\n}"

    class Config:
        frozen = True


class Create_thumbnailMutation(BaseModel):
    upload_thumbnail: Optional[ThumbnailFragment] = Field(alias="uploadThumbnail")

    class Arguments(BaseModel):
        rep: ID
        file: File

    class Meta:
        document = "fragment Thumbnail on Thumbnail {\n  id\n  image\n}\n\nmutation create_thumbnail($rep: ID!, $file: ImageFile!) {\n  uploadThumbnail(rep: $rep, file: $file) {\n    ...Thumbnail\n  }\n}"

    class Config:
        frozen = True


class Create_metricMutationCreatemetricRep(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID

    class Config:
        frozen = True


class Create_metricMutationCreatemetricCreator(BaseModel):
    """A reflection on the real User"""

    typename: Optional[Literal["User"]] = Field(alias="__typename")
    id: ID

    class Config:
        frozen = True


class Create_metricMutationCreatemetric(BaseModel):
    typename: Optional[Literal["Metric"]] = Field(alias="__typename")
    id: ID
    rep: Optional[Create_metricMutationCreatemetricRep]
    "The Representatoin this Metric belongs to"
    key: str
    "The Key"
    value: Optional[Dict]
    creator: Optional[Create_metricMutationCreatemetricCreator]
    created_at: str = Field(alias="createdAt")

    class Config:
        frozen = True


class Create_metricMutation(BaseModel):
    create_metric: Optional[Create_metricMutationCreatemetric] = Field(
        alias="createMetric"
    )
    "Creates a Representation"

    class Arguments(BaseModel):
        rep: Optional[ID] = None
        sample: Optional[ID] = None
        experiment: Optional[ID] = None
        key: str
        value: Dict

    class Meta:
        document = "mutation create_metric($rep: ID, $sample: ID, $experiment: ID, $key: String!, $value: GenericScalar!) {\n  createMetric(\n    rep: $rep\n    sample: $sample\n    experiment: $experiment\n    key: $key\n    value: $value\n  ) {\n    id\n    rep {\n      id\n    }\n    key\n    value\n    creator {\n      id\n    }\n    createdAt\n  }\n}"

    class Config:
        frozen = True


class Create_roiMutation(BaseModel):
    create_roi: Optional[ROIFragment] = Field(alias="createROI")
    "Creates a Sample"

    class Arguments(BaseModel):
        representation: ID
        vectors: List[Optional[InputVector]]
        creator: Optional[ID] = None
        type: RoiTypeInput

    class Meta:
        document = "fragment ROI on ROI {\n  id\n  vectors {\n    x\n    y\n    z\n  }\n  type\n  representation {\n    id\n  }\n  creator {\n    email\n    color\n  }\n}\n\nmutation create_roi($representation: ID!, $vectors: [InputVector]!, $creator: ID, $type: RoiTypeInput!) {\n  createROI(\n    representation: $representation\n    vectors: $vectors\n    type: $type\n    creator: $creator\n  ) {\n    ...ROI\n  }\n}"

    class Config:
        frozen = True


class From_dfMutation(BaseModel):
    from_df: Optional[TableFragment] = Field(alias="fromDf")
    "Creates a Representation"

    class Arguments(BaseModel):
        df: DataFrame

    class Meta:
        document = "fragment Table on Table {\n  id\n  name\n  tags\n  store\n  creator {\n    email\n  }\n  sample {\n    id\n  }\n  representation {\n    id\n  }\n  experiment {\n    id\n  }\n}\n\nmutation from_df($df: DataFrame!) {\n  fromDf(df: $df) {\n    ...Table\n  }\n}"

    class Config:
        frozen = True


class Create_sampleMutationCreatesampleCreator(BaseModel):
    """A reflection on the real User"""

    typename: Optional[Literal["User"]] = Field(alias="__typename")
    email: str

    class Config:
        frozen = True


class Create_sampleMutationCreatesample(Sample, BaseModel):
    """Samples are storage containers for representations. A Sample is to be understood analogous to a Biological Sample. It existed in Time (the time of acquisiton and experimental procedure),
    was measured in space (x,y,z) and in different modalities (c). Sample therefore provide a datacontainer where each Representation of
    the data shares the same dimensions. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    """

    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    id: ID
    name: str
    creator: Optional[Create_sampleMutationCreatesampleCreator]

    class Config:
        frozen = True


class Create_sampleMutation(BaseModel):
    create_sample: Optional[Create_sampleMutationCreatesample] = Field(
        alias="createSample"
    )
    "Creates a Sample\n    "

    class Arguments(BaseModel):
        name: Optional[str] = None
        creator: Optional[str] = None
        meta: Optional[Dict] = None
        experiments: Optional[List[Optional[ID]]] = None

    class Meta:
        document = "mutation create_sample($name: String, $creator: String, $meta: GenericScalar, $experiments: [ID]) {\n  createSample(\n    name: $name\n    creator: $creator\n    meta: $meta\n    experiments: $experiments\n  ) {\n    id\n    name\n    creator {\n      email\n    }\n  }\n}"

    class Config:
        frozen = True


class Create_experimentMutation(BaseModel):
    create_experiment: Optional[ExperimentFragment] = Field(alias="createExperiment")
    "Create an experiment (only signed in users)"

    class Arguments(BaseModel):
        name: str
        creator: Optional[str] = None
        meta: Optional[Dict] = None
        description: Optional[str] = None

    class Meta:
        document = "fragment Experiment on Experiment {\n  id\n  name\n  creator {\n    email\n  }\n  meta\n}\n\nmutation create_experiment($name: String!, $creator: String, $meta: GenericScalar, $description: String) {\n  createExperiment(\n    name: $name\n    creator: $creator\n    description: $description\n    meta: $meta\n  ) {\n    ...Experiment\n  }\n}"

    class Config:
        frozen = True


async def aget_omero_file(
    id: Optional[ID], rath: MikroRath = None
) -> OmeroFileFragment:
    """get_omero_file

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        OmeroFileFragment"""
    return (await aexecute(Get_omero_fileQuery, {"id": id}, rath=rath)).omerofile


def get_omero_file(id: Optional[ID], rath: MikroRath = None) -> OmeroFileFragment:
    """get_omero_file

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        OmeroFileFragment"""
    return execute(Get_omero_fileQuery, {"id": id}, rath=rath).omerofile


async def aexpand_omerofile(
    id: Optional[ID], rath: MikroRath = None
) -> OmeroFileFragment:
    """expand_omerofile

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        OmeroFileFragment"""
    return (await aexecute(Expand_omerofileQuery, {"id": id}, rath=rath)).omerofile


def expand_omerofile(id: Optional[ID], rath: MikroRath = None) -> OmeroFileFragment:
    """expand_omerofile

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        OmeroFileFragment"""
    return execute(Expand_omerofileQuery, {"id": id}, rath=rath).omerofile


async def asearch_omerofile(
    search: Optional[str], rath: MikroRath = None
) -> Optional[List[Optional[Search_omerofileQueryOmerofiles]]]:
    """search_omerofile


     omerofiles: My samples return all of the users samples attached to the current user

    Arguments:
        search (str): search
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Search_omerofileQuery"""
    return (
        await aexecute(Search_omerofileQuery, {"search": search}, rath=rath)
    ).omerofiles


def search_omerofile(
    search: Optional[str], rath: MikroRath = None
) -> Optional[List[Optional[Search_omerofileQueryOmerofiles]]]:
    """search_omerofile


     omerofiles: My samples return all of the users samples attached to the current user

    Arguments:
        search (str): search
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Search_omerofileQuery"""
    return execute(Search_omerofileQuery, {"search": search}, rath=rath).omerofiles


async def aexpand_representation(
    id: Optional[ID], rath: MikroRath = None
) -> RepresentationFragment:
    """expand_representation

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        RepresentationFragment"""
    return (
        await aexecute(Expand_representationQuery, {"id": id}, rath=rath)
    ).representation


def expand_representation(
    id: Optional[ID], rath: MikroRath = None
) -> RepresentationFragment:
    """expand_representation

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        RepresentationFragment"""
    return execute(Expand_representationQuery, {"id": id}, rath=rath).representation


async def aget_representation(
    id: Optional[ID], rath: MikroRath = None
) -> RepresentationFragment:
    """get_representation

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        RepresentationFragment"""
    return (
        await aexecute(Get_representationQuery, {"id": id}, rath=rath)
    ).representation


def get_representation(
    id: Optional[ID], rath: MikroRath = None
) -> RepresentationFragment:
    """get_representation

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        RepresentationFragment"""
    return execute(Get_representationQuery, {"id": id}, rath=rath).representation


async def asearch_representation(
    search: Optional[str] = None, rath: MikroRath = None
) -> Optional[List[Optional[Search_representationQueryRepresentations]]]:
    """search_representation


     representations: All represetations

    Arguments:
        search (Optional[str], optional): search.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Search_representationQuery"""
    return (
        await aexecute(Search_representationQuery, {"search": search}, rath=rath)
    ).representations


def search_representation(
    search: Optional[str] = None, rath: MikroRath = None
) -> Optional[List[Optional[Search_representationQueryRepresentations]]]:
    """search_representation


     representations: All represetations

    Arguments:
        search (Optional[str], optional): search.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Search_representationQuery"""
    return execute(
        Search_representationQuery, {"search": search}, rath=rath
    ).representations


async def aget_random_rep(rath: MikroRath = None) -> RepresentationFragment:
    """get_random_rep

    Get a single representation by ID

    Arguments:
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        RepresentationFragment"""
    return (await aexecute(Get_random_repQuery, {}, rath=rath)).random_representation


def get_random_rep(rath: MikroRath = None) -> RepresentationFragment:
    """get_random_rep

    Get a single representation by ID

    Arguments:
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        RepresentationFragment"""
    return execute(Get_random_repQuery, {}, rath=rath).random_representation


async def athumbnail(id: Optional[ID], rath: MikroRath = None) -> ThumbnailFragment:
    """Thumbnail

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ThumbnailFragment"""
    return (await aexecute(ThumbnailQuery, {"id": id}, rath=rath)).thumbnail


def thumbnail(id: Optional[ID], rath: MikroRath = None) -> ThumbnailFragment:
    """Thumbnail

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ThumbnailFragment"""
    return execute(ThumbnailQuery, {"id": id}, rath=rath).thumbnail


async def aexpand_thumbnail(
    id: Optional[ID], rath: MikroRath = None
) -> ThumbnailFragment:
    """expand_thumbnail

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ThumbnailFragment"""
    return (await aexecute(Expand_thumbnailQuery, {"id": id}, rath=rath)).thumbnail


def expand_thumbnail(id: Optional[ID], rath: MikroRath = None) -> ThumbnailFragment:
    """expand_thumbnail

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ThumbnailFragment"""
    return execute(Expand_thumbnailQuery, {"id": id}, rath=rath).thumbnail


async def aget_rois(
    representation: Optional[ID],
    type: Optional[List[Optional[RoiTypeInput]]] = None,
    rath: MikroRath = None,
) -> ROIFragment:
    """get_rois

    All represetations

    Arguments:
        representation (ID): representation
        type (Optional[List[Optional[RoiTypeInput]]], optional): type.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ROIFragment"""
    return (
        await aexecute(
            Get_roisQuery, {"representation": representation, "type": type}, rath=rath
        )
    ).rois


def get_rois(
    representation: Optional[ID],
    type: Optional[List[Optional[RoiTypeInput]]] = None,
    rath: MikroRath = None,
) -> ROIFragment:
    """get_rois

    All represetations

    Arguments:
        representation (ID): representation
        type (Optional[List[Optional[RoiTypeInput]]], optional): type.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ROIFragment"""
    return execute(
        Get_roisQuery, {"representation": representation, "type": type}, rath=rath
    ).rois


async def atable(id: Optional[ID], rath: MikroRath = None) -> TableFragment:
    """Table

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        TableFragment"""
    return (await aexecute(TableQuery, {"id": id}, rath=rath)).table


def table(id: Optional[ID], rath: MikroRath = None) -> TableFragment:
    """Table

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        TableFragment"""
    return execute(TableQuery, {"id": id}, rath=rath).table


async def aexpand_table(id: Optional[ID], rath: MikroRath = None) -> TableFragment:
    """expand_table

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        TableFragment"""
    return (await aexecute(Expand_tableQuery, {"id": id}, rath=rath)).table


def expand_table(id: Optional[ID], rath: MikroRath = None) -> TableFragment:
    """expand_table

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        TableFragment"""
    return execute(Expand_tableQuery, {"id": id}, rath=rath).table


async def asearch_tables(
    rath: MikroRath = None,
) -> Optional[List[Optional[Search_tablesQueryTables]]]:
    """search_tables


     tables: My samples return all of the users samples attached to the current user

    Arguments:
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Search_tablesQuery"""
    return (await aexecute(Search_tablesQuery, {}, rath=rath)).tables


def search_tables(
    rath: MikroRath = None,
) -> Optional[List[Optional[Search_tablesQueryTables]]]:
    """search_tables


     tables: My samples return all of the users samples attached to the current user

    Arguments:
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Search_tablesQuery"""
    return execute(Search_tablesQuery, {}, rath=rath).tables


async def aget_sample(id: Optional[ID], rath: MikroRath = None) -> SampleFragment:
    """get_sample

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        SampleFragment"""
    return (await aexecute(Get_sampleQuery, {"id": id}, rath=rath)).sample


def get_sample(id: Optional[ID], rath: MikroRath = None) -> SampleFragment:
    """get_sample

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        SampleFragment"""
    return execute(Get_sampleQuery, {"id": id}, rath=rath).sample


async def asearch_sample(
    search: Optional[str] = None, rath: MikroRath = None
) -> Optional[List[Optional[Search_sampleQuerySamples]]]:
    """search_sample


     samples: All Samples

    Arguments:
        search (Optional[str], optional): search.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Search_sampleQuery"""
    return (await aexecute(Search_sampleQuery, {"search": search}, rath=rath)).samples


def search_sample(
    search: Optional[str] = None, rath: MikroRath = None
) -> Optional[List[Optional[Search_sampleQuerySamples]]]:
    """search_sample


     samples: All Samples

    Arguments:
        search (Optional[str], optional): search.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Search_sampleQuery"""
    return execute(Search_sampleQuery, {"search": search}, rath=rath).samples


async def aexpand_sample(id: Optional[ID], rath: MikroRath = None) -> SampleFragment:
    """expand_sample

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        SampleFragment"""
    return (await aexecute(Expand_sampleQuery, {"id": id}, rath=rath)).sample


def expand_sample(id: Optional[ID], rath: MikroRath = None) -> SampleFragment:
    """expand_sample

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        SampleFragment"""
    return execute(Expand_sampleQuery, {"id": id}, rath=rath).sample


async def aget_experiment(
    id: Optional[ID], rath: MikroRath = None
) -> ExperimentFragment:
    """get_experiment

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ExperimentFragment"""
    return (await aexecute(Get_experimentQuery, {"id": id}, rath=rath)).experiment


def get_experiment(id: Optional[ID], rath: MikroRath = None) -> ExperimentFragment:
    """get_experiment

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ExperimentFragment"""
    return execute(Get_experimentQuery, {"id": id}, rath=rath).experiment


async def aexpand_experiment(
    id: Optional[ID], rath: MikroRath = None
) -> ExperimentFragment:
    """expand_experiment

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ExperimentFragment"""
    return (await aexecute(Expand_experimentQuery, {"id": id}, rath=rath)).experiment


def expand_experiment(id: Optional[ID], rath: MikroRath = None) -> ExperimentFragment:
    """expand_experiment

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ExperimentFragment"""
    return execute(Expand_experimentQuery, {"id": id}, rath=rath).experiment


async def asearch_experiment(
    search: Optional[str] = None, rath: MikroRath = None
) -> Optional[List[Optional[Search_experimentQueryExperiments]]]:
    """search_experiment


     experiments: All Samples

    Arguments:
        search (Optional[str], optional): search.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Search_experimentQuery"""
    return (
        await aexecute(Search_experimentQuery, {"search": search}, rath=rath)
    ).experiments


def search_experiment(
    search: Optional[str] = None, rath: MikroRath = None
) -> Optional[List[Optional[Search_experimentQueryExperiments]]]:
    """search_experiment


     experiments: All Samples

    Arguments:
        search (Optional[str], optional): search.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Search_experimentQuery"""
    return execute(Search_experimentQuery, {"search": search}, rath=rath).experiments


async def awatch_rois(
    representation: Optional[ID], rath: MikroRath = None
) -> AsyncIterator[Optional[Watch_roisSubscriptionRois]]:
    """watch_rois



    Arguments:
        representation (ID): representation
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Watch_roisSubscription"""
    async for event in asubscribe(
        Watch_roisSubscription, {"representation": representation}, rath=rath
    ):
        yield event.rois


def watch_rois(
    representation: Optional[ID], rath: MikroRath = None
) -> Iterator[Optional[Watch_roisSubscriptionRois]]:
    """watch_rois



    Arguments:
        representation (ID): representation
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Watch_roisSubscription"""
    for event in subscribe(
        Watch_roisSubscription, {"representation": representation}, rath=rath
    ):
        yield event.rois


async def awatch_samples(
    rath: MikroRath = None,
) -> AsyncIterator[Optional[Watch_samplesSubscriptionMysamples]]:
    """watch_samples



    Arguments:
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Watch_samplesSubscription"""
    async for event in asubscribe(Watch_samplesSubscription, {}, rath=rath):
        yield event.my_samples


def watch_samples(
    rath: MikroRath = None,
) -> Iterator[Optional[Watch_samplesSubscriptionMysamples]]:
    """watch_samples



    Arguments:
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Watch_samplesSubscription"""
    for event in subscribe(Watch_samplesSubscription, {}, rath=rath):
        yield event.my_samples


async def anegotiate(rath: MikroRath = None) -> Optional[Dict]:
    """negotiate



    Arguments:
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[Dict]"""
    return (await aexecute(NegotiateMutation, {}, rath=rath)).negotiate


def negotiate(rath: MikroRath = None) -> Optional[Dict]:
    """negotiate



    Arguments:
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[Dict]"""
    return execute(NegotiateMutation, {}, rath=rath).negotiate


async def aupload_bioimage(
    file: Optional[Upload], rath: MikroRath = None
) -> Optional[Upload_bioimageMutationUploadomerofile]:
    """upload_bioimage



    Arguments:
        file (Upload): file
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Upload_bioimageMutation"""
    return (
        await aexecute(Upload_bioimageMutation, {"file": file}, rath=rath)
    ).upload_omero_file


def upload_bioimage(
    file: Optional[Upload], rath: MikroRath = None
) -> Optional[Upload_bioimageMutationUploadomerofile]:
    """upload_bioimage



    Arguments:
        file (Upload): file
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Upload_bioimageMutation"""
    return execute(Upload_bioimageMutation, {"file": file}, rath=rath).upload_omero_file


async def acreate_size_feature(
    label: Optional[ID],
    size: Optional[float],
    creator: Optional[ID] = None,
    rath: MikroRath = None,
) -> Optional[Create_size_featureMutationCreatesizefeature]:
    """create_size_feature


     createSizeFeature: Creates a Sample

    Arguments:
        label (ID): label
        size (float): size
        creator (Optional[ID], optional): creator.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Create_size_featureMutation"""
    return (
        await aexecute(
            Create_size_featureMutation,
            {"label": label, "size": size, "creator": creator},
            rath=rath,
        )
    ).create_size_feature


def create_size_feature(
    label: Optional[ID],
    size: Optional[float],
    creator: Optional[ID] = None,
    rath: MikroRath = None,
) -> Optional[Create_size_featureMutationCreatesizefeature]:
    """create_size_feature


     createSizeFeature: Creates a Sample

    Arguments:
        label (ID): label
        size (float): size
        creator (Optional[ID], optional): creator.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Create_size_featureMutation"""
    return execute(
        Create_size_featureMutation,
        {"label": label, "size": size, "creator": creator},
        rath=rath,
    ).create_size_feature


async def acreate_label(
    instance: Optional[int],
    representation: Optional[ID],
    creator: Optional[ID],
    name: Optional[str] = None,
    rath: MikroRath = None,
) -> Optional[Create_labelMutationCreatelabel]:
    """create_label


     createLabel: Creates a Sample

    Arguments:
        instance (int): instance
        representation (ID): representation
        creator (ID): creator
        name (Optional[str], optional): name.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Create_labelMutation"""
    return (
        await aexecute(
            Create_labelMutation,
            {
                "instance": instance,
                "representation": representation,
                "creator": creator,
                "name": name,
            },
            rath=rath,
        )
    ).create_label


def create_label(
    instance: Optional[int],
    representation: Optional[ID],
    creator: Optional[ID],
    name: Optional[str] = None,
    rath: MikroRath = None,
) -> Optional[Create_labelMutationCreatelabel]:
    """create_label


     createLabel: Creates a Sample

    Arguments:
        instance (int): instance
        representation (ID): representation
        creator (ID): creator
        name (Optional[str], optional): name.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Create_labelMutation"""
    return execute(
        Create_labelMutation,
        {
            "instance": instance,
            "representation": representation,
            "creator": creator,
            "name": name,
        },
        rath=rath,
    ).create_label


async def afrom_xarray(
    xarray: Optional[XArray],
    name: Optional[str] = None,
    variety: Optional[RepresentationVarietyInput] = None,
    origins: Optional[List[Optional[ID]]] = None,
    tags: Optional[List[Optional[str]]] = None,
    sample: Optional[ID] = None,
    omero: Optional[OmeroRepresentationInput] = None,
    rath: MikroRath = None,
) -> RepresentationFragment:
    """from_xarray

    Creates a Representation

    Arguments:
        xarray (XArray): xarray
        name (Optional[str], optional): name.
        variety (Optional[RepresentationVarietyInput], optional): variety.
        origins (Optional[List[Optional[ID]]], optional): origins.
        tags (Optional[List[Optional[str]]], optional): tags.
        sample (Optional[ID], optional): sample.
        omero (Optional[OmeroRepresentationInput], optional): omero.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        RepresentationFragment"""
    return (
        await aexecute(
            From_xarrayMutation,
            {
                "xarray": xarray,
                "name": name,
                "variety": variety,
                "origins": origins,
                "tags": tags,
                "sample": sample,
                "omero": omero,
            },
            rath=rath,
        )
    ).from_x_array


def from_xarray(
    xarray: Optional[XArray],
    name: Optional[str] = None,
    variety: Optional[RepresentationVarietyInput] = None,
    origins: Optional[List[Optional[ID]]] = None,
    tags: Optional[List[Optional[str]]] = None,
    sample: Optional[ID] = None,
    omero: Optional[OmeroRepresentationInput] = None,
    rath: MikroRath = None,
) -> RepresentationFragment:
    """from_xarray

    Creates a Representation

    Arguments:
        xarray (XArray): xarray
        name (Optional[str], optional): name.
        variety (Optional[RepresentationVarietyInput], optional): variety.
        origins (Optional[List[Optional[ID]]], optional): origins.
        tags (Optional[List[Optional[str]]], optional): tags.
        sample (Optional[ID], optional): sample.
        omero (Optional[OmeroRepresentationInput], optional): omero.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        RepresentationFragment"""
    return execute(
        From_xarrayMutation,
        {
            "xarray": xarray,
            "name": name,
            "variety": variety,
            "origins": origins,
            "tags": tags,
            "sample": sample,
            "omero": omero,
        },
        rath=rath,
    ).from_x_array


async def adouble_upload(
    xarray: Optional[XArray],
    name: Optional[str] = None,
    origins: Optional[List[Optional[ID]]] = None,
    tags: Optional[List[Optional[str]]] = None,
    sample: Optional[ID] = None,
    omero: Optional[OmeroRepresentationInput] = None,
    rath: MikroRath = None,
) -> Double_uploadMutation:
    """double_upload


     x: Creates a Representation
     y: Creates a Representation

    Arguments:
        xarray (XArray): xarray
        name (Optional[str], optional): name.
        origins (Optional[List[Optional[ID]]], optional): origins.
        tags (Optional[List[Optional[str]]], optional): tags.
        sample (Optional[ID], optional): sample.
        omero (Optional[OmeroRepresentationInput], optional): omero.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Double_uploadMutation"""
    return (
        await aexecute(
            Double_uploadMutation,
            {
                "xarray": xarray,
                "name": name,
                "origins": origins,
                "tags": tags,
                "sample": sample,
                "omero": omero,
            },
            rath=rath,
        )
    ).from_x_array


def double_upload(
    xarray: Optional[XArray],
    name: Optional[str] = None,
    origins: Optional[List[Optional[ID]]] = None,
    tags: Optional[List[Optional[str]]] = None,
    sample: Optional[ID] = None,
    omero: Optional[OmeroRepresentationInput] = None,
    rath: MikroRath = None,
) -> Double_uploadMutation:
    """double_upload


     x: Creates a Representation
     y: Creates a Representation

    Arguments:
        xarray (XArray): xarray
        name (Optional[str], optional): name.
        origins (Optional[List[Optional[ID]]], optional): origins.
        tags (Optional[List[Optional[str]]], optional): tags.
        sample (Optional[ID], optional): sample.
        omero (Optional[OmeroRepresentationInput], optional): omero.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Double_uploadMutation"""
    return execute(
        Double_uploadMutation,
        {
            "xarray": xarray,
            "name": name,
            "origins": origins,
            "tags": tags,
            "sample": sample,
            "omero": omero,
        },
        rath=rath,
    ).from_x_array


async def acreate_thumbnail(
    rep: Optional[ID], file: Optional[File], rath: MikroRath = None
) -> ThumbnailFragment:
    """create_thumbnail



    Arguments:
        rep (ID): rep
        file (File): file
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ThumbnailFragment"""
    return (
        await aexecute(Create_thumbnailMutation, {"rep": rep, "file": file}, rath=rath)
    ).upload_thumbnail


def create_thumbnail(
    rep: Optional[ID], file: Optional[File], rath: MikroRath = None
) -> ThumbnailFragment:
    """create_thumbnail



    Arguments:
        rep (ID): rep
        file (File): file
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ThumbnailFragment"""
    return execute(
        Create_thumbnailMutation, {"rep": rep, "file": file}, rath=rath
    ).upload_thumbnail


async def acreate_metric(
    key: Optional[str],
    value: Optional[Dict],
    rep: Optional[ID] = None,
    sample: Optional[ID] = None,
    experiment: Optional[ID] = None,
    rath: MikroRath = None,
) -> Optional[Create_metricMutationCreatemetric]:
    """create_metric


     createMetric: Creates a Representation

    Arguments:
        key (str): key
        value (Dict): value
        rep (Optional[ID], optional): rep.
        sample (Optional[ID], optional): sample.
        experiment (Optional[ID], optional): experiment.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Create_metricMutation"""
    return (
        await aexecute(
            Create_metricMutation,
            {
                "rep": rep,
                "sample": sample,
                "experiment": experiment,
                "key": key,
                "value": value,
            },
            rath=rath,
        )
    ).create_metric


def create_metric(
    key: Optional[str],
    value: Optional[Dict],
    rep: Optional[ID] = None,
    sample: Optional[ID] = None,
    experiment: Optional[ID] = None,
    rath: MikroRath = None,
) -> Optional[Create_metricMutationCreatemetric]:
    """create_metric


     createMetric: Creates a Representation

    Arguments:
        key (str): key
        value (Dict): value
        rep (Optional[ID], optional): rep.
        sample (Optional[ID], optional): sample.
        experiment (Optional[ID], optional): experiment.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Create_metricMutation"""
    return execute(
        Create_metricMutation,
        {
            "rep": rep,
            "sample": sample,
            "experiment": experiment,
            "key": key,
            "value": value,
        },
        rath=rath,
    ).create_metric


async def acreate_roi(
    representation: Optional[ID],
    vectors: Optional[List[Optional[InputVector]]],
    type: Optional[RoiTypeInput],
    creator: Optional[ID] = None,
    rath: MikroRath = None,
) -> ROIFragment:
    """create_roi

    Creates a Sample

    Arguments:
        representation (ID): representation
        vectors (List[Optional[InputVector]]): vectors
        type (RoiTypeInput): type
        creator (Optional[ID], optional): creator.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ROIFragment"""
    return (
        await aexecute(
            Create_roiMutation,
            {
                "representation": representation,
                "vectors": vectors,
                "creator": creator,
                "type": type,
            },
            rath=rath,
        )
    ).create_roi


def create_roi(
    representation: Optional[ID],
    vectors: Optional[List[Optional[InputVector]]],
    type: Optional[RoiTypeInput],
    creator: Optional[ID] = None,
    rath: MikroRath = None,
) -> ROIFragment:
    """create_roi

    Creates a Sample

    Arguments:
        representation (ID): representation
        vectors (List[Optional[InputVector]]): vectors
        type (RoiTypeInput): type
        creator (Optional[ID], optional): creator.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ROIFragment"""
    return execute(
        Create_roiMutation,
        {
            "representation": representation,
            "vectors": vectors,
            "creator": creator,
            "type": type,
        },
        rath=rath,
    ).create_roi


async def afrom_df(df: Optional[DataFrame], rath: MikroRath = None) -> TableFragment:
    """from_df

    Creates a Representation

    Arguments:
        df (DataFrame): df
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        TableFragment"""
    return (await aexecute(From_dfMutation, {"df": df}, rath=rath)).from_df


def from_df(df: Optional[DataFrame], rath: MikroRath = None) -> TableFragment:
    """from_df

    Creates a Representation

    Arguments:
        df (DataFrame): df
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        TableFragment"""
    return execute(From_dfMutation, {"df": df}, rath=rath).from_df


async def acreate_sample(
    name: Optional[str] = None,
    creator: Optional[str] = None,
    meta: Optional[Dict] = None,
    experiments: Optional[List[Optional[ID]]] = None,
    rath: MikroRath = None,
) -> Optional[Create_sampleMutationCreatesample]:
    """create_sample


     createSample: Creates a Sample


    Arguments:
        name (Optional[str], optional): name.
        creator (Optional[str], optional): creator.
        meta (Optional[Dict], optional): meta.
        experiments (Optional[List[Optional[ID]]], optional): experiments.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Create_sampleMutation"""
    return (
        await aexecute(
            Create_sampleMutation,
            {
                "name": name,
                "creator": creator,
                "meta": meta,
                "experiments": experiments,
            },
            rath=rath,
        )
    ).create_sample


def create_sample(
    name: Optional[str] = None,
    creator: Optional[str] = None,
    meta: Optional[Dict] = None,
    experiments: Optional[List[Optional[ID]]] = None,
    rath: MikroRath = None,
) -> Optional[Create_sampleMutationCreatesample]:
    """create_sample


     createSample: Creates a Sample


    Arguments:
        name (Optional[str], optional): name.
        creator (Optional[str], optional): creator.
        meta (Optional[Dict], optional): meta.
        experiments (Optional[List[Optional[ID]]], optional): experiments.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Create_sampleMutation"""
    return execute(
        Create_sampleMutation,
        {"name": name, "creator": creator, "meta": meta, "experiments": experiments},
        rath=rath,
    ).create_sample


async def acreate_experiment(
    name: Optional[str],
    creator: Optional[str] = None,
    meta: Optional[Dict] = None,
    description: Optional[str] = None,
    rath: MikroRath = None,
) -> ExperimentFragment:
    """create_experiment

    Create an experiment (only signed in users)

    Arguments:
        name (str): name
        creator (Optional[str], optional): creator.
        meta (Optional[Dict], optional): meta.
        description (Optional[str], optional): description.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ExperimentFragment"""
    return (
        await aexecute(
            Create_experimentMutation,
            {
                "name": name,
                "creator": creator,
                "meta": meta,
                "description": description,
            },
            rath=rath,
        )
    ).create_experiment


def create_experiment(
    name: Optional[str],
    creator: Optional[str] = None,
    meta: Optional[Dict] = None,
    description: Optional[str] = None,
    rath: MikroRath = None,
) -> ExperimentFragment:
    """create_experiment

    Create an experiment (only signed in users)

    Arguments:
        name (str): name
        creator (Optional[str], optional): creator.
        meta (Optional[Dict], optional): meta.
        description (Optional[str], optional): description.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ExperimentFragment"""
    return execute(
        Create_experimentMutation,
        {"name": name, "creator": creator, "meta": meta, "description": description},
        rath=rath,
    ).create_experiment

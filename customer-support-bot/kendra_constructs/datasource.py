import json
from constructs import Construct

from aws_cdk import (
    aws_iam as iam,
    Stack,
    aws_kendra as kendra,
    custom_resources as cr,
    CustomResource,
)
from datetime import datetime


default_schedule = "cron(0 0 1 * ? *)"
default_schedule = ""


class CRKendraCrawlerV2Datasource(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        service_token,
        index_id,
        role_arn,
        name,
        seed_urls,
        s3_seed_url,
        url_inclusion_patterns,
        url_exclusion_patterns,
        description="default description",
        schedule=default_schedule,
        language_code="en",
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        if seed_urls:
            seed_url_connections = [{"seedUrl": s} for s in seed_urls]
            connection_configuration = dict(
                repositoryEndpointMetadata=dict(
                    s3SeedUrl=None,
                    siteMapUrls=None,
                    seedUrlConnections=seed_url_connections,
                    s3SiteMapUrl=None,
                    authentication="NoAuthentication",
                )
            )

        if s3_seed_url:
            connection_configuration = dict(
                repositoryEndpointMetadata=dict(
                    s3SeedUrl=s3_seed_url,
                    siteMapUrls=None,
                    seedUrlConnections=None,
                    s3SiteMapUrl=None,
                    authentication="NoAuthentication",
                )
            )

        repository_configurations = dict(
            attachment=dict(
                fieldMappings=[
                    dict(
                        dataSourceFieldName="category",
                        indexFieldName="_category",
                        indexFieldType="STRING",
                    ),
                    dict(
                        dataSourceFieldName="sourceUrl",
                        indexFieldName="_source_uri",
                        indexFieldType="STRING",
                    ),
                ]
            ),
            webPage=dict(
                fieldMappings=[
                    dict(
                        dataSourceFieldName="category",
                        indexFieldName="_category",
                        indexFieldType="STRING",
                    ),
                    dict(
                        dataSourceFieldName="sourceUrl",
                        indexFieldName="_source_uri",
                        indexFieldType="STRING",
                    ),
                ]
            ),
        )

        additiona_properties = dict(
            inclusionFileIndexPatterns=[],
            rateLimit="300",
            maxFileSize="50",
            crawlDepth="1",
            crawlAllDomain=False,
            crawlSubDomain=False,
            inclusionURLIndexPatterns=url_inclusion_patterns,
            exclusionFileIndexPatterns=[],
            proxy={},
            exclusionURLCrawlPatterns=url_exclusion_patterns,
            exclusionURLIndexPatterns=url_exclusion_patterns,
            crawlAttachments=False,
            honorRobots=True,
            inclusionURLCrawlPatterns=url_inclusion_patterns,
            crawlDomainsOnly=True,
            maxLinksPerUrl="100",
        )

        template = dict(
            connectionConfiguration=connection_configuration,
            enableIdentityCrawler=False,
            syncMode="FORCED_FULL_CRAWL",
            additionalProperties=additiona_properties,
            type="WEBCRAWLERV2",
            version="1.0.0",
            repositoryConfigurations=repository_configurations,
        )

        cr_docs_ds = CustomResource(
            self,
            "CR2",
            resource_type="Custom::CRDataSource",
            service_token=service_token,
            properties=dict(
                index_id=index_id,
                role_arn=role_arn,
                name=name,
                description=description,
                type="TEMPLATE",
                template=json.dumps(template),
                schedule=schedule,
                language_code=language_code,
            ),
        )


class KendraCrawlerDatasource(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        index_id,
        role_arn,
        name,
        seed_urls,
        url_inclusion_patterns,
        url_exclusion_patterns,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.data_source = kendra.CfnDataSource(
            self,
            "WC",
            index_id=index_id,
            name=name,
            type="WEBCRAWLER",
            data_source_configuration=kendra.CfnDataSource.DataSourceConfigurationProperty(
                web_crawler_configuration=kendra.CfnDataSource.WebCrawlerConfigurationProperty(
                    urls=kendra.CfnDataSource.WebCrawlerUrlsProperty(
                        seed_url_configuration=kendra.CfnDataSource.WebCrawlerSeedUrlConfigurationProperty(
                            seed_urls=seed_urls,
                        )
                    ),
                    crawl_depth=10,
                    url_exclusion_patterns=url_exclusion_patterns,
                    url_inclusion_patterns=url_inclusion_patterns,
                ),
            ),
            role_arn=role_arn,
            schedule=default_schedule,
        )


import json
from constructs import Construct

from aws_cdk import (
    aws_iam as iam,
    Stack,
    aws_kendra as kendra,
    custom_resources as cr,
    CustomResource,
)
from datetime import datetime


default_schedule = "cron(0 0 1 * ? *)"
default_schedule = ""


class CRKendraCrawlerV2Datasource(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        service_token,
        index_id,
        role_arn,
        name,
        seed_urls,
        s3_seed_url,
        url_inclusion_patterns,
        url_exclusion_patterns,
        description="default description",
        schedule=default_schedule,
        language_code="en",
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        if seed_urls:
            seed_url_connections = [{"seedUrl": s} for s in seed_urls]
            connection_configuration = dict(
                repositoryEndpointMetadata=dict(
                    s3SeedUrl=None,
                    siteMapUrls=None,
                    seedUrlConnections=seed_url_connections,
                    s3SiteMapUrl=None,
                    authentication="NoAuthentication",
                )
            )

        if s3_seed_url:
            connection_configuration = dict(
                repositoryEndpointMetadata=dict(
                    s3SeedUrl=s3_seed_url,
                    siteMapUrls=None,
                    seedUrlConnections=None,
                    s3SiteMapUrl=None,
                    authentication="NoAuthentication",
                )
            )

        repository_configurations = dict(
            attachment=dict(
                fieldMappings=[
                    dict(
                        dataSourceFieldName="category",
                        indexFieldName="_category",
                        indexFieldType="STRING",
                    ),
                    dict(
                        dataSourceFieldName="sourceUrl",
                        indexFieldName="_source_uri",
                        indexFieldType="STRING",
                    ),
                ]
            ),
            webPage=dict(
                fieldMappings=[
                    dict(
                        dataSourceFieldName="category",
                        indexFieldName="_category",
                        indexFieldType="STRING",
                    ),
                    dict(
                        dataSourceFieldName="sourceUrl",
                        indexFieldName="_source_uri",
                        indexFieldType="STRING",
                    ),
                ]
            ),
        )

        additiona_properties = dict(
            inclusionFileIndexPatterns=[],
            rateLimit="300",
            maxFileSize="50",
            crawlDepth="1",
            crawlAllDomain=False,
            crawlSubDomain=False,
            inclusionURLIndexPatterns=url_inclusion_patterns,
            exclusionFileIndexPatterns=[],
            proxy={},
            exclusionURLCrawlPatterns=url_exclusion_patterns,
            exclusionURLIndexPatterns=url_exclusion_patterns,
            crawlAttachments=False,
            honorRobots=True,
            inclusionURLCrawlPatterns=url_inclusion_patterns,
            crawlDomainsOnly=True,
            maxLinksPerUrl="100",
        )

        template = dict(
            connectionConfiguration=connection_configuration,
            enableIdentityCrawler=False,
            syncMode="FORCED_FULL_CRAWL",
            additionalProperties=additiona_properties,
            type="WEBCRAWLERV2",
            version="1.0.0",
            repositoryConfigurations=repository_configurations,
        )

        cr_docs_ds = CustomResource(
            self,
            "CR2",
            resource_type="Custom::CRDataSource",
            service_token=service_token,
            properties=dict(
                index_id=index_id,
                role_arn=role_arn,
                name=name,
                description=description,
                type="TEMPLATE",
                template=json.dumps(template),
                schedule=schedule,
                language_code=language_code,
            ),
        )


class CRKendraS3Datasource(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        service_token,
        index_id,
        role_arn,
        name,
        bucket_name,
        inclusion_patterns,
        inclusion_prefixes,
        metadata_files_prefix = None,
        exclusion_patterns = [],
        exclusion_prefixes = [],
        description="default description",
        schedule=default_schedule,
        language_code="en",
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)


        connection_configuration = dict(
            repositoryEndpointMetadata=dict(
                BucketName=bucket_name
            )
        )

        repository_configurations = dict(
            document=dict(
                fieldMappings=[
                    dict(
                        dataSourceFieldName="s3_document_id",
                        indexFieldName="s3_document_id",
                        indexFieldType="STRING",
                    )
                ]
            )
        )
        additiona_properties = dict(
            inclusionPrefixes=inclusion_prefixes,
            exclusionPatterns=exclusion_patterns,
            inclusionPatterns=inclusion_patterns,
            maxFileSizeInMegaBytes ="100",
            #exclusionPrefixes=exclusion_prefixes,
        )

        if metadata_files_prefix:
            additiona_properties = dict(**additiona_properties, metadataFilesPrefix = metadata_files_prefix)

        template = dict(
            connectionConfiguration=connection_configuration,
            syncMode="FORCED_FULL_CRAWL",
            additionalProperties=additiona_properties,
            type="S3",
            version="1.0.0",
            repositoryConfigurations=repository_configurations,
        )


        ds = CustomResource(
            self,
            "S3DS",
            resource_type="Custom::S3DataSource",
            service_token=service_token,
            properties=dict(
                index_id=index_id,
                role_arn=role_arn,
                name=name,
                description=description,
                type="TEMPLATE",
                template=json.dumps(template),
                schedule=schedule,
                language_code=language_code,
            ),
        )
